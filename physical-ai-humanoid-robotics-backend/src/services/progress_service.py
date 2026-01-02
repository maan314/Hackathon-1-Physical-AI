from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List, Optional
from fastapi import HTTPException, status
from datetime import datetime

from src.models.progress import Progress, ProgressCreate, ProgressUpdate, UserProgress, QuizAttempt, LearningPath
from src.models.content import Content
from src.database.database import get_db


class ProgressService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_or_update_progress(self, progress_data: ProgressCreate) -> Progress:
        # Check if progress record already exists
        result = await self.db.execute(
            select(Progress)
            .where(Progress.user_id == progress_data.user_id)
            .where(Progress.content_id == progress_data.content_id)
        )
        existing_progress = result.scalars().first()

        if existing_progress:
            # Update existing progress
            if progress_data.progress_percentage is not None:
                existing_progress.progress_percentage = progress_data.progress_percentage
            if progress_data.time_spent is not None:
                existing_progress.time_spent = progress_data.time_spent
            if progress_data.is_completed is not None:
                existing_progress.is_completed = progress_data.is_completed

            existing_progress.updated_at = datetime.utcnow()
            self.db.add(existing_progress)
            await self.db.commit()
            await self.db.refresh(existing_progress)
            return existing_progress
        else:
            # Create new progress record
            db_progress = Progress(
                id=str(hash(f"progress_{progress_data.user_id}_{progress_data.content_id}_{datetime.utcnow()}"))[:12],
                user_id=progress_data.user_id,
                content_id=progress_data.content_id,
                progress_percentage=progress_data.progress_percentage,
                time_spent=progress_data.time_spent,
                is_completed=progress_data.is_completed,
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow()
            )

            self.db.add(db_progress)
            await self.db.commit()
            await self.db.refresh(db_progress)
            return db_progress

    async def get_user_progress(self, user_id: str, content_id: str) -> Optional[UserProgress]:
        result = await self.db.execute(
            select(Progress)
            .where(Progress.user_id == user_id)
            .where(Progress.content_id == content_id)
        )
        progress = result.scalars().first()

        if not progress:
            return None

        return UserProgress(
            user_id=progress.user_id,
            content_id=progress.content_id,
            progress_percentage=progress.progress_percentage,
            time_spent=progress.time_spent,
            is_completed=progress.is_completed,
            created_at=progress.created_at,
            updated_at=progress.updated_at
        )

    async def get_content_progress(self, content_id: str) -> List[UserProgress]:
        result = await self.db.execute(
            select(Progress).where(Progress.content_id == content_id)
        )
        progresses = result.scalars().all()

        user_progresses = []
        for progress in progresses:
            user_progress = UserProgress(
                user_id=progress.user_id,
                content_id=progress.content_id,
                progress_percentage=progress.progress_percentage,
                time_spent=progress.time_spent,
                is_completed=progress.is_completed,
                created_at=progress.created_at,
                updated_at=progress.updated_at
            )
            user_progresses.append(user_progress)

        return user_progresses

    async def get_user_all_progress(self, user_id: str) -> List[UserProgress]:
        result = await self.db.execute(
            select(Progress).where(Progress.user_id == user_id)
        )
        progresses = result.scalars().all()

        user_progresses = []
        for progress in progresses:
            user_progress = UserProgress(
                user_id=progress.user_id,
                content_id=progress.content_id,
                progress_percentage=progress.progress_percentage,
                time_spent=progress.time_spent,
                is_completed=progress.is_completed,
                created_at=progress.created_at,
                updated_at=progress.updated_at
            )
            user_progresses.append(user_progress)

        return user_progresses

    async def update_progress(self, user_id: str, content_id: str, progress_update: ProgressUpdate) -> Optional[Progress]:
        result = await self.db.execute(
            select(Progress)
            .where(Progress.user_id == user_id)
            .where(Progress.content_id == content_id)
        )
        progress = result.scalars().first()

        if not progress:
            return None

        # Update progress fields
        if progress_update.progress_percentage is not None:
            progress.progress_percentage = progress_update.progress_percentage
        if progress_update.time_spent is not None:
            progress.time_spent = progress_update.time_spent
        if progress_update.is_completed is not None:
            progress.is_completed = progress_update.is_completed

        progress.updated_at = datetime.utcnow()
        self.db.add(progress)
        await self.db.commit()
        await self.db.refresh(progress)

        return progress

    async def get_user_completion_stats(self, user_id: str) -> dict:
        """
        Get user's overall completion statistics
        """
        all_progress = await self.get_user_all_progress(user_id)

        total_content = len(all_progress)
        completed_content = sum(1 for p in all_progress if p.is_completed)
        in_progress_content = sum(1 for p in all_progress if p.progress_percentage > 0 and not p.is_completed)

        total_time_spent = sum(p.time_spent for p in all_progress)
        avg_progress = sum(p.progress_percentage for p in all_progress) / total_content if total_content > 0 else 0

        return {
            "total_content": total_content,
            "completed_content": completed_content,
            "in_progress_content": in_progress_content,
            "total_time_spent": total_time_spent,
            "average_progress": avg_progress,
            "completion_percentage": (completed_content / total_content * 100) if total_content > 0 else 0
        }

    async def create_quiz_attempt(self, user_id: str, content_id: str, score: float, total_questions: int, correct_answers: int, time_taken: int) -> QuizAttempt:
        """
        Record a quiz attempt
        """
        quiz_attempt = QuizAttempt(
            id=str(hash(f"quiz_{user_id}_{content_id}_{datetime.utcnow()}"))[:12],
            user_id=user_id,
            content_id=content_id,
            score=score,
            total_questions=total_questions,
            correct_answers=correct_answers,
            time_taken=time_taken,
            created_at=datetime.utcnow()
        )

        self.db.add(quiz_attempt)
        await self.db.commit()
        await self.db.refresh(quiz_attempt)

        return quiz_attempt

    async def get_user_quiz_attempts(self, user_id: str, content_id: Optional[str] = None) -> List[QuizAttempt]:
        """
        Get quiz attempts for a user, optionally filtered by content
        """
        query = select(QuizAttempt).where(QuizAttempt.user_id == user_id)
        if content_id:
            query = query.where(QuizAttempt.content_id == content_id)

        result = await self.db.execute(query)
        attempts = result.scalars().all()

        return attempts

    async def create_learning_path(self, user_id: str, name: str, description: str, content_ids: List[str]) -> LearningPath:
        """
        Create a custom learning path for a user
        """
        learning_path = LearningPath(
            id=str(hash(f"path_{user_id}_{name}_{datetime.utcnow()}"))[:12],
            user_id=user_id,
            name=name,
            description=description,
            content_ids=content_ids,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )

        self.db.add(learning_path)
        await self.db.commit()
        await self.db.refresh(learning_path)

        return learning_path

    async def get_user_learning_paths(self, user_id: str) -> List[LearningPath]:
        """
        Get all learning paths for a user
        """
        result = await self.db.execute(
            select(LearningPath).where(LearningPath.user_id == user_id)
        )
        paths = result.scalars().all()

        return paths

    async def get_learning_path(self, path_id: str) -> Optional[LearningPath]:
        """
        Get a specific learning path by ID
        """
        result = await self.db.execute(
            select(LearningPath).where(LearningPath.id == path_id)
        )
        path = result.scalars().first()

        return path

    async def update_learning_path(self, path_id: str, name: Optional[str] = None, description: Optional[str] = None, content_ids: Optional[List[str]] = None) -> Optional[LearningPath]:
        """
        Update a learning path
        """
        result = await self.db.execute(
            select(LearningPath).where(LearningPath.id == path_id)
        )
        path = result.scalars().first()

        if not path:
            return None

        if name is not None:
            path.name = name
        if description is not None:
            path.description = description
        if content_ids is not None:
            path.content_ids = content_ids

        path.updated_at = datetime.utcnow()
        self.db.add(path)
        await self.db.commit()
        await self.db.refresh(path)

        return path

    async def delete_learning_path(self, path_id: str) -> bool:
        """
        Delete a learning path
        """
        result = await self.db.execute(
            select(LearningPath).where(LearningPath.id == path_id)
        )
        path = result.scalars().first()

        if not path:
            return False

        await self.db.delete(path)
        await self.db.commit()
        return True