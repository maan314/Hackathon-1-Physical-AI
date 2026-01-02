from pydantic import BaseModel
from typing import Optional, Union
from datetime import datetime
from enum import Enum

class SoftwareExperience(str, Enum):
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"

class HardwareExperience(str, Enum):
    NONE = "none"
    BASIC = "basic"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"

# Define types that accept both string and enum
SoftwareExperienceType = Union[SoftwareExperience, str, None]
HardwareExperienceType = Union[HardwareExperience, str, None]

class UserBase(BaseModel):
    email: str
    name: str
    software_experience: Optional[SoftwareExperienceType] = None
    hardware_experience: Optional[HardwareExperienceType] = None

class UserCreate(UserBase):
    password: str

    class Config:
        use_enum_values = True

class UserUpdate(BaseModel):
    software_experience: Optional[SoftwareExperience] = None
    hardware_experience: Optional[HardwareExperience] = None

class User(UserBase):
    id: str
    hashed_password: str
    created_at: datetime
    last_login: Optional[datetime] = None

    class Config:
        from_attributes = True