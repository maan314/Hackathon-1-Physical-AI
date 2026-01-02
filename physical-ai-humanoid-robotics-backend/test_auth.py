#!/usr/bin/env python3
"""Test script to debug the authentication service directly"""

import asyncio
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__)))

from src.database.database import get_db, engine
from src.database.models import Base
from src.services.auth_service import AuthService
from src.models.auth import RegisterRequest
from src.models.user import UserCreate


async def test_registration():
    # Create tables first if they don't exist
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    # Get a database session
    async for db in get_db():
        try:
            # Create auth service
            auth_service = AuthService(db)

            # Create registration data
            register_data = RegisterRequest(
                email="test@example.com",
                password="password123",
                name="Test User"
            )

            # Create UserCreate object (this is where the error might occur)
            user_create = UserCreate(
                email=register_data.email,
                password=register_data.password,
                name=register_data.name,
                software_experience=register_data.software_experience,
                hardware_experience=register_data.hardware_experience
            )

            print("UserCreate object created successfully")
            print(f"User data: {user_create}")

            # Try to register the user
            result = await auth_service.register_user(user_create)
            print(f"Registration successful: {result}")

        except Exception as e:
            print(f"Error during registration: {e}")
            import traceback
            traceback.print_exc()
        break  # Exit the async for loop after one iteration


if __name__ == "__main__":
    asyncio.run(test_registration())