from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List, Optional
from fastapi import HTTPException, status
from datetime import datetime

from src.models.content import Content, ContentCreate, ContentUpdate, Module, Chapter
from src.database.database import get_db


class ContentService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_content(self, content_data: ContentCreate) -> Content:
        db_content = Content(
            id=str(hash(f"{content_data.title}{datetime.utcnow()}"))[:12],  # Simple ID generation
            title=content_data.title,
            content=content_data.content,
            content_type=content_data.content_type,
            module_type=content_data.module_type,
            order=content_data.order,
            parent_id=content_data.parent_id,
            prerequisites=content_data.prerequisites,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
            author_id=content_data.author_id if hasattr(content_data, 'author_id') else None
        )

        self.db.add(db_content)
        await self.db.commit()
        await self.db.refresh(db_content)

        return db_content

    async def get_content(self, content_id: str) -> Optional[Content]:
        result = await self.db.execute(
            select(Content).where(Content.id == content_id)
        )
        content = result.scalars().first()
        return content

    async def get_content_by_module_type(self, module_type: str) -> List[Content]:
        result = await self.db.execute(
            select(Content).where(Content.module_type == module_type).order_by(Content.order)
        )
        contents = result.scalars().all()
        return contents

    async def update_content(self, content_id: str, content_update: ContentUpdate) -> Optional[Content]:
        result = await self.db.execute(
            select(Content).where(Content.id == content_id)
        )
        content = result.scalars().first()

        if not content:
            return None

        # Update content fields
        if content_update.title is not None:
            content.title = content_update.title
        if content_update.content is not None:
            content.content = content_update.content
        if content_update.content_type is not None:
            content.content_type = content_update.content_type
        if content_update.order is not None:
            content.order = content_update.order
        if content_update.parent_id is not None:
            content.parent_id = content_update.parent_id

        content.updated_at = datetime.utcnow()
        self.db.add(content)
        await self.db.commit()
        await self.db.refresh(content)

        return content

    async def delete_content(self, content_id: str) -> bool:
        result = await self.db.execute(
            select(Content).where(Content.id == content_id)
        )
        content = result.scalars().first()

        if not content:
            return False

        await self.db.delete(content)
        await self.db.commit()
        return True

    async def get_modules(self) -> List[Module]:
        # In a real implementation, this would fetch from the database
        # For now, we'll return the predefined modules
        modules = [
            Module(
                id="module-1",
                title="The Robotic Nervous System (ROS 2)",
                description="Embodied Control & Middleware",
                module_type="ros_2",
                order=1,
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow()
            ),
            Module(
                id="module-2",
                title="The Digital Twin (Gazebo & Unity)",
                description="Physics, Simulation & Interaction",
                module_type="gazebo_unity",
                order=2,
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow()
            ),
            Module(
                id="module-3",
                title="The AI-Robot Brain (NVIDIA Isaac™)",
                description="AI Integration & Transfer",
                module_type="nvidia_isaac",
                order=3,
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow()
            ),
            Module(
                id="module-4",
                title="Vision–Language–Action (VLA)",
                description="Multimodal AI & Safety",
                module_type="vla",
                order=4,
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow()
            ),
            Module(
                id="module-5",
                title="Capstone — Autonomous Humanoid",
                description="Full System Integration",
                module_type="humanoid",
                order=5,
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow()
            )
        ]
        return modules

    async def get_chapters_by_module(self, module_id: str) -> List[Chapter]:
        # This would fetch chapters from the database in a real implementation
        # For now, we'll return predefined chapters based on the module
        chapters = []
        if module_id == "module-1":
            chapters = [
                Chapter(
                    id="ch-1-1",
                    title="Embodied Control and Middleware",
                    module_id=module_id,
                    order=1,
                    content="Introduction to embodied control systems...",
                    created_at=datetime.utcnow(),
                    updated_at=datetime.utcnow()
                ),
                Chapter(
                    id="ch-1-2",
                    title="ROS 2 Nodes, Topics, Services, Actions",
                    module_id=module_id,
                    order=2,
                    content="Understanding ROS 2 communication patterns...",
                    created_at=datetime.utcnow(),
                    updated_at=datetime.utcnow()
                ),
                Chapter(
                    id="ch-1-3",
                    title="Python Agents & ROS Controllers",
                    module_id=module_id,
                    order=3,
                    content="Building Python-based ROS agents...",
                    created_at=datetime.utcnow(),
                    updated_at=datetime.utcnow()
                ),
                Chapter(
                    id="ch-1-4",
                    title="URDF for Humanoid Anatomy",
                    module_id=module_id,
                    order=4,
                    content="Creating URDF models for humanoid robots...",
                    created_at=datetime.utcnow(),
                    updated_at=datetime.utcnow()
                )
            ]
        # Similar logic for other modules...
        return chapters