from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from datetime import datetime
from enum import Enum


class DifficultyLevel(str, Enum):
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"


class LearningStyle(str, Enum):
    VISUAL = "visual"
    AUDITORY = "auditory"
    READING_WRITING = "reading_writing"
    KINESTHETIC = "kinesthetic"


class PersonalizationProfileBase(BaseModel):
    user_id: str
    preferred_difficulty: Optional[DifficultyLevel] = None
    learning_style: Optional[LearningStyle] = None
    software_experience: Optional[str] = None  # beginner, intermediate, advanced
    hardware_experience: Optional[str] = None  # none, basic, intermediate, advanced
    interests: Optional[List[str]] = []
    goals: Optional[List[str]] = []
    preferences: Optional[Dict[str, Any]] = {}


class PersonalizationProfileCreate(PersonalizationProfileBase):
    pass


class PersonalizationProfileUpdate(BaseModel):
    preferred_difficulty: Optional[DifficultyLevel] = None
    learning_style: Optional[LearningStyle] = None
    software_experience: Optional[str] = None
    hardware_experience: Optional[str] = None
    interests: Optional[List[str]] = None
    goals: Optional[List[str]] = None
    preferences: Optional[Dict[str, Any]] = None


class PersonalizationProfile(PersonalizationProfileBase):
    id: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class ContentPersonalization(BaseModel):
    id: str
    content_id: str
    personalized_content: str
    difficulty_level: Optional[DifficultyLevel] = None
    target_audience: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class PersonalizationRecommendation(BaseModel):
    id: str
    user_id: str
    content_id: str
    recommendation_type: str  # curriculum, difficulty, learning_path
    reason: str
    confidence: float
    created_at: datetime

    class Config:
        from_attributes = True