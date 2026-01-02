import asyncio
from src.database.database import engine, Base
from src.database.models import User, ChatSession, ChatMessage


async def create_tables():
    """Create all database tables."""
    async with engine.begin() as conn:
        # Create all tables
        await conn.run_sync(Base.metadata.create_all)
    print("Database tables created successfully!")


if __name__ == "__main__":
    asyncio.run(create_tables())