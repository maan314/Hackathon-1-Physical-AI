from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List, Optional, Dict, Any
from fastapi import HTTPException, status
from datetime import datetime
import json

from src.models.personalization import (
    PersonalizationProfile, PersonalizationProfileCreate, PersonalizationProfileUpdate,
    ContentPersonalization, PersonalizationRecommendation, DifficultyLevel
)
from src.models.user import User
from src.models.content import Content
from src.database.database import get_db


class PersonalizationService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_or_update_profile(self, profile_data: PersonalizationProfileCreate) -> PersonalizationProfile:
        # Check if profile already exists
        result = await self.db.execute(
            select(PersonalizationProfile).where(PersonalizationProfile.user_id == profile_data.user_id)
        )
        existing_profile = result.scalars().first()

        if existing_profile:
            # Update existing profile
            if profile_data.preferred_difficulty is not None:
                existing_profile.preferred_difficulty = profile_data.preferred_difficulty
            if profile_data.learning_style is not None:
                existing_profile.learning_style = profile_data.learning_style
            if profile_data.software_experience is not None:
                existing_profile.software_experience = profile_data.software_experience
            if profile_data.hardware_experience is not None:
                existing_profile.hardware_experience = profile_data.hardware_experience
            if profile_data.interests is not None:
                existing_profile.interests = profile_data.interests
            if profile_data.goals is not None:
                existing_profile.goals = profile_data.goals
            if profile_data.preferences is not None:
                existing_profile.preferences = profile_data.preferences

            existing_profile.updated_at = datetime.utcnow()
            self.db.add(existing_profile)
            await self.db.commit()
            await self.db.refresh(existing_profile)
            return existing_profile
        else:
            # Create new profile
            db_profile = PersonalizationProfile(
                id=str(hash(f"profile_{profile_data.user_id}_{datetime.utcnow()}"))[:12],
                user_id=profile_data.user_id,
                preferred_difficulty=profile_data.preferred_difficulty,
                learning_style=profile_data.learning_style,
                software_experience=profile_data.software_experience,
                hardware_experience=profile_data.hardware_experience,
                interests=profile_data.interests,
                goals=profile_data.goals,
                preferences=profile_data.preferences,
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow()
            )

            self.db.add(db_profile)
            await self.db.commit()
            await self.db.refresh(db_profile)
            return db_profile

    async def get_profile(self, user_id: str) -> Optional[PersonalizationProfile]:
        result = await self.db.execute(
            select(PersonalizationProfile).where(PersonalizationProfile.user_id == user_id)
        )
        profile = result.scalars().first()
        return profile

    async def update_profile(self, user_id: str, profile_update: PersonalizationProfileUpdate) -> Optional[PersonalizationProfile]:
        result = await self.db.execute(
            select(PersonalizationProfile).where(PersonalizationProfile.user_id == user_id)
        )
        profile = result.scalars().first()

        if not profile:
            return None

        # Update profile fields
        if profile_update.preferred_difficulty is not None:
            profile.preferred_difficulty = profile_update.preferred_difficulty
        if profile_update.learning_style is not None:
            profile.learning_style = profile_update.learning_style
        if profile_update.software_experience is not None:
            profile.software_experience = profile_update.software_experience
        if profile_update.hardware_experience is not None:
            profile.hardware_experience = profile_update.hardware_experience
        if profile_update.interests is not None:
            profile.interests = profile_update.interests
        if profile_update.goals is not None:
            profile.goals = profile_update.goals
        if profile_update.preferences is not None:
            profile.preferences = profile_update.preferences

        profile.updated_at = datetime.utcnow()
        self.db.add(profile)
        await self.db.commit()
        await self.db.refresh(profile)

        return profile

    async def get_personalized_content(self, user_id: str, content_id: str) -> Optional[ContentPersonalization]:
        # Get user profile
        profile = await self.get_profile(user_id)
        if not profile:
            return None

        # Get original content
        result = await self.db.execute(
            select(Content).where(Content.id == content_id)
        )
        original_content = result.scalars().first()
        if not original_content:
            return None

        # Get user info to determine experience level
        user_result = await self.db.execute(
            select(User).where(User.id == user_id)
        )
        user = user_result.scalars().first()

        # Generate personalized content based on user profile
        personalized_content = await self._generate_personalized_content(
            original_content.content,
            profile,
            user
        )

        # Create or return existing personalized content
        result = await self.db.execute(
            select(ContentPersonalization).where(
                ContentPersonalization.content_id == content_id
            ).where(
                ContentPersonalization.target_audience == user_id
            )
        )
        existing_personalized = result.scalars().first()

        if existing_personalized:
            existing_personalized.personalized_content = personalized_content
            existing_personalized.difficulty_level = profile.preferred_difficulty
            existing_personalized.updated_at = datetime.utcnow()
            self.db.add(existing_personalized)
            await self.db.commit()
            await self.db.refresh(existing_personalized)
            return existing_personalized
        else:
            db_personalized = ContentPersonalization(
                id=str(hash(f"personalized_{content_id}_{user_id}"))[:12],
                content_id=content_id,
                personalized_content=personalized_content,
                difficulty_level=profile.preferred_difficulty,
                target_audience=user_id,
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow()
            )

            self.db.add(db_personalized)
            await self.db.commit()
            await self.db.refresh(db_personalized)
            return db_personalized

    async def _generate_personalized_content(self, original_content: str, profile: PersonalizationProfile, user: User) -> str:
        """
        Generate personalized content based on user profile and experience
        In a real implementation, this would use an LLM to rewrite content
        """
        # Determine user's experience level
        user_exp = "beginner"
        if user and user.software_experience and user.hardware_experience:
            # Use the higher of the two experience levels
            if user.software_experience == "advanced" or user.hardware_experience == "advanced":
                user_exp = "advanced"
            elif user.software_experience == "intermediate" or user.hardware_experience == "intermediate":
                user_exp = "intermediate"

        # Add personalization context to the content
        prefix = f"Personalized for {user_exp} level:\n\n"
        return prefix + original_content

    async def get_recommendations(self, user_id: str) -> List[PersonalizationRecommendation]:
        # Get user profile
        profile = await self.get_profile(user_id)
        if not profile:
            return []

        # Generate recommendations based on user profile
        recommendations = []

        # Example: recommend content based on interests
        if profile.interests:
            for i, interest in enumerate(profile.interests[:3]):  # Limit to 3 recommendations
                rec = PersonalizationRecommendation(
                    id=f"rec_{user_id}_{i}",
                    user_id=user_id,
                    content_id=f"content_{interest}",
                    recommendation_type="curriculum",
                    reason=f"Recommended based on your interest in {interest}",
                    confidence=0.8,
                    created_at=datetime.utcnow()
                )
                recommendations.append(rec)

        # Example: recommend difficulty level
        if profile.preferred_difficulty:
            rec = PersonalizationRecommendation(
                id=f"rec_diff_{user_id}",
                user_id=user_id,
                content_id="difficulty_level",
                recommendation_type="difficulty",
                reason=f"Recommended difficulty level: {profile.preferred_difficulty}",
                confidence=0.9,
                created_at=datetime.utcnow()
            )
            recommendations.append(rec)

        return recommendations

    async def get_personalized_learning_path(self, user_id: str) -> List[str]:
        """
        Generate a personalized learning path based on user profile
        """
        profile = await self.get_profile(user_id)
        if not profile:
            # Return default learning path
            return [
                "module-1-chapter-1", "module-1-chapter-2", "module-1-chapter-3", "module-1-chapter-4",
                "module-2-chapter-1", "module-2-chapter-2", "module-2-chapter-3", "module-2-chapter-4",
                "module-3-chapter-1", "module-3-chapter-2", "module-3-chapter-3", "module-3-chapter-4",
                "module-4-chapter-1", "module-4-chapter-2", "module-4-chapter-3", "module-4-chapter-4",
                "module-5-chapter-1", "module-5-chapter-2", "module-5-chapter-3", "module-5-chapter-4"
            ]

        # Generate path based on experience level
        base_path = [
            "module-1-chapter-1", "module-1-chapter-2", "module-1-chapter-3", "module-1-chapter-4",
            "module-2-chapter-1", "module-2-chapter-2", "module-2-chapter-3", "module-2-chapter-4",
            "module-3-chapter-1", "module-3-chapter-2", "module-3-chapter-3", "module-3-chapter-4",
            "module-4-chapter-1", "module-4-chapter-2", "module-4-chapter-3", "module-4-chapter-4",
            "module-5-chapter-1", "module-5-chapter-2", "module-5-chapter-3", "module-5-chapter-4"
        ]

        # Adjust path based on experience
        if profile.software_experience == "advanced" or profile.hardware_experience == "advanced":
            # Advanced users might skip some introductory content
            return base_path
        elif profile.software_experience == "intermediate" or profile.hardware_experience == "intermediate":
            # Intermediate users follow standard path
            return base_path
        else:
            # Beginner users follow standard path with additional resources
            return base_path