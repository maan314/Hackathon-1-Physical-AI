from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from enum import Enum


class ModuleType(str, Enum):
    ROS_2 = "ros_2"
    GAZEBO_UNITY = "gazebo_unity"
    NVIDIA_ISAAC = "nvidia_isaac"
    VLA = "vla"
    HUMANOID = "humanoid"


class ContentType(str, Enum):
    CHAPTER = "chapter"
    SECTION = "section"
    EXAMPLE = "example"
    EXERCISE = "exercise"
    VIDEO = "video"
    CODE_SNIPPET = "code_snippet"


class ContentBase(BaseModel):
    title: str
    content: str
    content_type: ContentType
    module_type: ModuleType
    order: int
    parent_id: Optional[str] = None
    prerequisites: Optional[List[str]] = []


class ContentCreate(ContentBase):
    pass


class ContentUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    content_type: Optional[ContentType] = None
    order: Optional[int] = None
    parent_id: Optional[str] = None


class Content(ContentBase):
    id: str
    created_at: datetime
    updated_at: datetime
    author_id: Optional[str] = None

    class Config:
        from_attributes = True


class Module(BaseModel):
    id: str
    title: str
    description: str
    module_type: ModuleType
    order: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class Chapter(BaseModel):
    id: str
    title: str
    module_id: str
    order: int
    content: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True