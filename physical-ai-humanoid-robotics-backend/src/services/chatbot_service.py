from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List, Optional, Dict, Any
from fastapi import HTTPException, status
from datetime import datetime
import asyncio
import openai
from qdrant_client import QdrantClient
from qdrant_client.http import models
import uuid

from src.models.chatbot import (
    ChatMessageCreate, ChatSessionCreate,
    ChatSessionUpdate, ChatResponse, RetrievalResult, ChatbotConfig
)
from src.database.models import ChatMessage, ChatSession
from src.models.content import Content
from src.database.database import get_db


class ChatbotService:
    def __init__(self, db: AsyncSession, qdrant_client: QdrantClient, openai_client: openai.AsyncOpenAI):
        self.db = db
        self.qdrant_client = qdrant_client
        self.openai_client = openai_client
        self.config = ChatbotConfig()

    async def create_chat_session(self, session_data: ChatSessionCreate) -> ChatSession:
        db_session = ChatSession(
            id=str(uuid.uuid4()),
            user_id=session_data.user_id,
            title=session_data.title,
            context=session_data.context,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )

        self.db.add(db_session)
        await self.db.commit()
        await self.db.refresh(db_session)

        return db_session

    async def get_chat_session(self, session_id: str) -> Optional[ChatSession]:
        result = await self.db.execute(
            select(ChatSession).where(ChatSession.id == session_id)
        )
        session = result.scalars().first()
        return session

    async def update_chat_session(self, session_id: str, session_update: ChatSessionUpdate) -> Optional[ChatSession]:
        result = await self.db.execute(
            select(ChatSession).where(ChatSession.id == session_id)
        )
        session = result.scalars().first()

        if not session:
            return None

        if session_update.title is not None:
            session.title = session_update.title
        if session_update.context is not None:
            session.context = session_update.context

        session.updated_at = datetime.utcnow()
        self.db.add(session)
        await self.db.commit()
        await self.db.refresh(session)

        return session

    async def add_message_to_session(self, session_id: str, message_data: ChatMessageCreate) -> ChatMessage:
        db_message = ChatMessage(
            id=str(uuid.uuid4()),
            chat_session_id=session_id,
            role=message_data.role,
            content=message_data.content,
            user_id=message_data.user_id,
            created_at=datetime.utcnow()
        )

        self.db.add(db_message)
        await self.db.commit()
        await self.db.refresh(db_message)

        return db_message

    async def get_session_messages(self, session_id: str) -> List[ChatMessage]:
        result = await self.db.execute(
            select(ChatMessage)
            .where(ChatMessage.chat_session_id == session_id)
            .order_by(ChatMessage.created_at)
        )
        messages = result.scalars().all()
        return messages

    async def get_relevant_content(self, query: str, top_k: int = 5) -> List[RetrievalResult]:
        """
        Retrieve relevant content from the vector database using Qdrant
        """
        try:
            # Search in Qdrant for relevant content
            search_results = self.qdrant_client.search(
                collection_name="textbook_content",
                query_text=query,
                limit=top_k
            )

            results = []
            for hit in search_results:
                result = RetrievalResult(
                    content_id=hit.payload.get("content_id", ""),
                    content=hit.payload.get("content", ""),
                    similarity_score=hit.score,
                    source=hit.payload.get("source", "unknown")
                )
                results.append(result)

            return results
        except Exception as e:
            print(f"Error retrieving content from Qdrant: {e}")
            # Fallback: return empty results
            return []

    async def process_query_with_rag(self, query: str, session_id: str, user_id: Optional[str] = None) -> ChatResponse:
        """
        Process a user query using RAG (Retrieval-Augmented Generation)
        """
        # Add user message to session
        user_message = ChatMessageCreate(
            role="user",
            content=query,
            user_id=user_id
        )
        await self.add_message_to_session(session_id, user_message)

        # Retrieve relevant content
        relevant_content = await self.get_relevant_content(query, self.config.retrieval_top_k)

        if not relevant_content:
            # If no relevant content found, return a default response
            response_text = "I couldn't find specific information about that topic in the textbook. Please check the relevant chapters or ask a more specific question."
            sources = []
        else:
            # Build context from retrieved content
            context_parts = []
            sources = []
            for content in relevant_content:
                context_parts.append(content.content)
                sources.append(content.source)

            context = "\n\n".join(context_parts)

            # Create the full prompt for the LLM
            prompt = f"""
            You are an AI assistant for the Physical AI & Humanoid Robotics Textbook.
            Answer the user's question based on the following context from the textbook:

            Context: {context}

            User question: {query}

            Please provide a helpful answer based on the textbook content. If the context doesn't contain the information needed, say so politely.
            """

            try:
                # Call OpenAI API to generate response
                response = await self.openai_client.chat.completions.create(
                    model=self.config.model_name,
                    messages=[{"role": "user", "content": prompt}],
                    temperature=self.config.temperature,
                    max_tokens=self.config.max_tokens
                )

                response_text = response.choices[0].message.content
            except Exception as e:
                print(f"Error calling OpenAI API: {e}")
                response_text = "I encountered an error while processing your request. Please try again."

        # Add assistant message to session
        assistant_message = ChatMessageCreate(
            role="assistant",
            content=response_text,
            user_id=user_id
        )
        await self.add_message_to_session(session_id, assistant_message)

        # Extract reasoning steps (simplified for this example)
        reasoning_steps = [
            "Retrieved relevant textbook content",
            "Formulated context-aware prompt",
            "Generated response using AI model"
        ]

        return ChatResponse(
            message=response_text,
            sources=sources,
            confidence=0.8,  # Placeholder confidence score
            reasoning_steps=reasoning_steps
        )

    async def enforce_selected_text(self, query: str, selected_text: str) -> ChatResponse:
        """
        Enforce that the response is based on the selected text
        """
        prompt = f"""
        You are an AI assistant for the Physical AI & Humanoid Robotics Textbook.
        The user has selected the following text and has a question about it:

        Selected text: {selected_text}

        User question: {query}

        Please provide an answer that is directly based on the selected text.
        """

        try:
            response = await self.openai_client.chat.completions.create(
                model=self.config.model_name,
                messages=[{"role": "user", "content": prompt}],
                temperature=self.config.temperature,
                max_tokens=self.config.max_tokens
            )

            response_text = response.choices[0].message.content
        except Exception as e:
            print(f"Error calling OpenAI API: {e}")
            response_text = "I encountered an error while processing your request. Please try again."

        reasoning_steps = [
            "Focused on selected text",
            "Generated response based on selected text"
        ]

        return ChatResponse(
            message=response_text,
            sources=["selected_text"],
            confidence=0.9,  # Higher confidence for selected text enforcement
            reasoning_steps=reasoning_steps
        )

    async def get_chat_history(self, session_id: str, limit: int = 10) -> List[ChatMessage]:
        """
        Get recent chat history for a session
        """
        result = await self.db.execute(
            select(ChatMessage)
            .where(ChatMessage.chat_session_id == session_id)
            .order_by(ChatMessage.created_at.desc())
            .limit(limit)
        )
        messages = result.scalars().all()
        # Reverse to return in chronological order
        return list(reversed(messages))

    async def get_all_sessions(self, user_id: str) -> List[ChatSession]:
        """
        Get all chat sessions for a user
        """
        result = await self.db.execute(
            select(ChatSession)
            .where(ChatSession.user_id == user_id)
            .order_by(ChatSession.created_at.desc())
        )
        sessions = result.scalars().all()
        return sessions