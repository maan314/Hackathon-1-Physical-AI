from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import Optional
from datetime import datetime, timedelta
from fastapi import HTTPException, status

from src.database.models import User
from src.models.user import UserCreate, UserUpdate
from src.models.auth import TokenResponse, UserProfile
from src.utils.security import verify_password, get_password_hash, create_access_token
from src.database.database import get_db


class AuthService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def register_user(self, user_data: UserCreate) -> UserProfile:
        # Check if user already exists
        result = await self.db.execute(
            select(User).where(User.email == user_data.email)
        )
        existing_user = result.scalars().first()

        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User with this email already exists"
            )

        # Create new user
        hashed_password = get_password_hash(user_data.password)
        db_user = User(
            email=user_data.email,
            name=user_data.name,
            hashed_password=hashed_password,
            software_experience=user_data.software_experience,
            hardware_experience=user_data.hardware_experience,
            created_at=datetime.utcnow(),
            last_login=None
        )

        self.db.add(db_user)
        await self.db.commit()
        await self.db.refresh(db_user)

        return UserProfile(
            id=db_user.id,
            email=db_user.email,
            name=db_user.name,
            software_experience=db_user.software_experience,
            hardware_experience=db_user.hardware_experience,
            created_at=db_user.created_at,
            last_login=db_user.last_login
        )

    async def authenticate_user(self, email: str, password: str) -> Optional[TokenResponse]:
        # Find user by email
        result = await self.db.execute(
            select(User).where(User.email == email)
        )
        user = result.scalars().first()

        if not user or not verify_password(password, user.hashed_password):
            return None

        # Update last login
        user.last_login = datetime.utcnow()
        self.db.add(user)
        await self.db.commit()

        # Create access token
        access_token_expires = timedelta(minutes=30)
        access_token = create_access_token(
            data={"sub": user.id}, expires_delta=access_token_expires
        )

        return TokenResponse(
            access_token=access_token,
            token_type="bearer",
            user_id=user.id,
            expires_at=datetime.utcnow() + access_token_expires
        )

    async def get_user_profile(self, user_id: str) -> Optional[UserProfile]:
        result = await self.db.execute(
            select(User).where(User.id == user_id)
        )
        user = result.scalars().first()

        if not user:
            return None

        return UserProfile(
            id=user.id,
            email=user.email,
            name=user.name,
            software_experience=user.software_experience,
            hardware_experience=user.hardware_experience,
            created_at=user.created_at,
            last_login=user.last_login
        )

    async def update_user_profile(self, user_id: str, user_update: UserUpdate) -> Optional[UserProfile]:
        result = await self.db.execute(
            select(User).where(User.id == user_id)
        )
        user = result.scalars().first()

        if not user:
            return None

        # Update user fields
        if user_update.software_experience is not None:
            user.software_experience = user_update.software_experience
        if user_update.hardware_experience is not None:
            user.hardware_experience = user_update.hardware_experience

        self.db.add(user)
        await self.db.commit()
        await self.db.refresh(user)

        return UserProfile(
            id=user.id,
            email=user.email,
            name=user.name,
            software_experience=user.software_experience,
            hardware_experience=user.hardware_experience,
            created_at=user.created_at,
            last_login=user.last_login
        )