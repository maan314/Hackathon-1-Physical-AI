from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from enum import Enum


class TranslationStatus(str, Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"


class TranslationRequestBase(BaseModel):
    content_id: str
    source_language: str
    target_language: str
    content_type: str  # text, code, equation, etc.
    preserve_formatting: bool = True


class TranslationRequestCreate(TranslationRequestBase):
    pass


class TranslationRequest(TranslationRequestBase):
    id: str
    user_id: Optional[str] = None
    status: TranslationStatus
    translated_content: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    completed_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class TranslationPair(BaseModel):
    id: str
    content_id: str
    source_content: str
    translated_content: str
    source_language: str
    target_language: str
    created_at: datetime

    class Config:
        from_attributes = True


class SupportedLanguage(BaseModel):
    language_code: str
    language_name: str
    is_enabled: bool
    supports_formatting: bool

    class Config:
        from_attributes = True


class TranslationConfig(BaseModel):
    default_source_language: str = "en"
    default_target_language: str = "ur"
    max_content_length: int = 10000
    enable_caching: bool = True
    preserve_code_blocks: bool = True
    preserve_equations: bool = True

    class Config:
        from_attributes = True