from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


class ProgressBase(BaseModel):
    user_id: str
    content_id: str
    progress_percentage: float
    time_spent: int  # in seconds
    is_completed: bool


class ProgressCreate(ProgressBase):
    pass


class ProgressUpdate(BaseModel):
    progress_percentage: Optional[float] = None
    time_spent: Optional[int] = None
    is_completed: Optional[bool] = None


class Progress(ProgressBase):
    id: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class UserProgress(BaseModel):
    user_id: str
    content_id: str
    progress_percentage: float
    time_spent: int
    is_completed: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class QuizAttempt(BaseModel):
    id: str
    user_id: str
    content_id: str
    score: float
    total_questions: int
    correct_answers: int
    time_taken: int  # in seconds
    created_at: datetime

    class Config:
        from_attributes = True


class LearningPath(BaseModel):
    id: str
    user_id: str
    name: str
    description: str
    content_ids: List[str]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True