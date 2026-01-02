from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession
import openai
from qdrant_client import QdrantClient
import os
import uuid

from src.services.chatbot_service import ChatbotService
from src.models.chatbot import ChatSessionCreate, ChatSessionUpdate, ChatSession, ChatResponse
from src.database.database import get_db
from src.routes.auth import get_current_user
from src.utils.security import settings, verify_token, TokenData


router = APIRouter()

# Optional authentication dependency
security = HTTPBearer(auto_error=False)

async def get_current_user_optional(credentials: HTTPAuthorizationCredentials = Depends(security)) -> TokenData:
    if credentials is None:
        return None
    token_data = verify_token(credentials.credentials)
    return token_data or None


@router.post("/sessions", response_model=ChatSession)
async def create_chat_session(
    session_data: ChatSessionCreate,
    current_user: TokenData = Depends(get_current_user_optional),
    db: AsyncSession = Depends(get_db)
):
    # Initialize Qdrant and OpenAI clients (in a real app, these would be properly configured)
    qdrant_client = QdrantClient(":memory:")  # For demo purposes
    openai_client = openai.AsyncOpenAI(api_key=settings.OPENAI_API_KEY)  # Use API key from settings

    chatbot_service = ChatbotService(db, qdrant_client, openai_client)
    # For anonymous sessions, user_id can be None or we can generate a temporary ID
    if current_user:
        session_data.user_id = current_user.user_id
    else:
        session_data.user_id = session_data.user_id or f"anonymous_{uuid.uuid4()}"
    return await chatbot_service.create_chat_session(session_data)


@router.get("/sessions/{session_id}", response_model=ChatSession)
async def get_chat_session(
    session_id: str,
    current_user: TokenData = Depends(get_current_user_optional),
    db: AsyncSession = Depends(get_db)
):
    # Initialize Qdrant and OpenAI clients (in a real app, these would be properly configured)
    qdrant_client = QdrantClient(":memory:")  # For demo purposes
    openai_client = openai.AsyncOpenAI(api_key=settings.OPENAI_API_KEY)  # Use API key from settings

    chatbot_service = ChatbotService(db, qdrant_client, openai_client)
    session = await chatbot_service.get_chat_session(session_id)

    if not session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Chat session not found"
        )

    # Only check ownership if the session belongs to a registered user (not anonymous)
    if session.user_id and not session.user_id.startswith("anonymous_"):
        if not current_user or session.user_id != current_user.user_id:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Chat session not found"
            )

    return session


@router.put("/sessions/{session_id}", response_model=ChatSession)
async def update_chat_session(
    session_id: str,
    session_update: ChatSessionUpdate,
    current_user=Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    # Initialize Qdrant and OpenAI clients (in a real app, these would be properly configured)
    qdrant_client = QdrantClient(":memory:")  # For demo purposes
    openai_client = openai.AsyncOpenAI(api_key=settings.OPENAI_API_KEY)  # Use API key from settings

    chatbot_service = ChatbotService(db, qdrant_client, openai_client)
    updated_session = await chatbot_service.update_chat_session(session_id, session_update)

    if not updated_session or updated_session.user_id != current_user.user_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Chat session not found"
        )

    return updated_session


@router.post("/sessions/{session_id}/query", response_model=ChatResponse)
async def process_query_with_rag(
    session_id: str,
    query: str,
    current_user: TokenData = Depends(get_current_user_optional),
    db: AsyncSession = Depends(get_db)
):
    # Initialize Qdrant and OpenAI clients (in a real app, these would be properly configured)
    qdrant_client = QdrantClient(":memory:")  # For demo purposes
    openai_client = openai.AsyncOpenAI(api_key=settings.OPENAI_API_KEY)  # Use API key from settings

    chatbot_service = ChatbotService(db, qdrant_client, openai_client)
    user_id = current_user.user_id if current_user else f"anonymous_{uuid.uuid4()}"
    return await chatbot_service.process_query_with_rag(query, session_id, user_id)


@router.post("/enforce-selected-text", response_model=ChatResponse)
async def enforce_selected_text(
    query: str,
    selected_text: str,
    current_user=Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    # Initialize Qdrant and OpenAI clients (in a real app, these would be properly configured)
    qdrant_client = QdrantClient(":memory:")  # For demo purposes
    openai_client = openai.AsyncOpenAI(api_key=settings.OPENAI_API_KEY)  # Use API key from settings

    chatbot_service = ChatbotService(db, qdrant_client, openai_client)
    return await chatbot_service.enforce_selected_text(query, selected_text)


@router.get("/sessions/{session_id}/history", response_model=list)
async def get_chat_history(
    session_id: str,
    limit: int = 10,
    current_user=Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    # Initialize Qdrant and OpenAI clients (in a real app, these would be properly configured)
    qdrant_client = QdrantClient(":memory:")  # For demo purposes
    openai_client = openai.AsyncOpenAI(api_key=settings.OPENAI_API_KEY)  # Use API key from settings

    chatbot_service = ChatbotService(db, qdrant_client, openai_client)
    session = await chatbot_service.get_chat_session(session_id)

    if not session or session.user_id != current_user.user_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Chat session not found"
        )

    return await chatbot_service.get_chat_history(session_id, limit)


@router.get("/sessions/", response_model=list)
async def get_all_sessions(
    current_user=Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    # Initialize Qdrant and OpenAI clients (in a real app, these would be properly configured)
    qdrant_client = QdrantClient(":memory:")  # For demo purposes
    openai_client = openai.AsyncOpenAI(api_key=settings.OPENAI_API_KEY)  # Use API key from settings

    chatbot_service = ChatbotService(db, qdrant_client, openai_client)
    return await chatbot_service.get_all_sessions(current_user.user_id)