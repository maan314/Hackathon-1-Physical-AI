from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from pydantic_settings import BaseSettings, SettingsConfigDict
import os
from urllib.parse import urlparse


class Settings(BaseSettings):
    DATABASE_URL: str = "sqlite:///./test.db"  # Default to SQLite for development

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore"  # ← ignore extra environment variables
    )


settings = Settings()

# Use SQLite for development, PostgreSQL for production
db_url = settings.DATABASE_URL

# Check if we're using PostgreSQL and convert to async driver
if db_url.startswith("postgresql://"):
    # Replace postgresql:// with postgresql+asyncpg:// and handle query parameters
    parsed = urlparse(db_url)
    if parsed.query:
        # For PostgreSQL URLs with query parameters like sslmode, we need to handle them properly
        db_url = f"postgresql+asyncpg://{parsed.netloc}{parsed.path}?{parsed.query}"
    else:
        db_url = db_url.replace("postgresql://", "postgresql+asyncpg://", 1)
elif db_url.startswith("sqlite://"):
    # For SQLite, use aiosqlite driver
    if not db_url.startswith("sqlite+aiosqlite"):
        db_url = db_url.replace("sqlite://", "sqlite+aiosqlite://", 1)

engine = create_async_engine(db_url)
AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

Base = declarative_base()


async def get_db():
    async with AsyncSessionLocal() as db:
        try:
            yield db
        finally:
            await db.close()