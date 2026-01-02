from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from datetime import datetime
from enum import Enum


class MessageRole(str, Enum):
    USER = "user"
    ASSISTANT = "assistant"
    SYSTEM = "system"


class ChatMessageBase(BaseModel):
    role: MessageRole
    content: str
    user_id: Optional[str] = None


class ChatMessageCreate(ChatMessageBase):
    pass


class ChatMessage(ChatMessageBase):
    id: str
    chat_session_id: str
    created_at: datetime

    class Config:
        from_attributes = True


class ChatSessionBase(BaseModel):
    user_id: Optional[str] = None
    title: str
    context: Optional[Dict[str, Any]] = {}


class ChatSessionCreate(ChatSessionBase):
    pass


class ChatSessionUpdate(BaseModel):
    title: Optional[str] = None
    context: Optional[Dict[str, Any]] = None


class ChatSession(ChatSessionBase):
    id: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class ChatResponse(BaseModel):
    message: str
    sources: List[str]
    confidence: float
    reasoning_steps: List[str]

    class Config:
        from_attributes = True


class RetrievalResult(BaseModel):
    content_id: str
    content: str
    similarity_score: float
    source: str

    class Config:
        from_attributes = True


class ChatbotConfig(BaseModel):
    model_name: str = "gpt-4"
    temperature: float = 0.7
    max_tokens: int = 1000
    retrieval_top_k: int = 5
    enforce_selected_text: bool = True

    class Config:
        from_attributes = True