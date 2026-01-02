from pydantic_settings import BaseSettings, SettingsConfigDict
from datetime import datetime, timedelta
from typing import Optional
import jwt
from pydantic_settings import BaseSettings
from pydantic import Field, BaseModel
import os


# Password hashing with fallback
def _setup_password_context():
    """Set up password hashing context with fallback"""
    try:
        from passlib.context import CryptContext
        # Try bcrypt first
        pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

        def verify_password(plain_password: str, hashed_password: str) -> bool:
            return pwd_context.verify(plain_password, hashed_password)

        def get_password_hash(password: str) -> str:
            # Bcrypt has a 72-byte password length limit
            # Truncate password if it exceeds the limit
            if len(password.encode('utf-8')) > 72:
                password = password.encode('utf-8')[:72].decode('utf-8', errors='ignore')
            return pwd_context.hash(password)

        return verify_password, get_password_hash
    except Exception:
        # Fallback to pbkdf2 if bcrypt is not available or has issues
        from passlib.context import CryptContext
        pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")

        def verify_password(plain_password: str, hashed_password: str) -> bool:
            return pwd_context.verify(plain_password, hashed_password)

        def get_password_hash(password: str) -> str:
            return pwd_context.hash(password)

        return verify_password, get_password_hash


# Set up the actual functions
verify_password, get_password_hash = _setup_password_context()

class Settings(BaseSettings):
    SECRET_KEY: str = os.getenv("SECRET_KEY", "fallback_secret_key_for_development")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
     # 🤖 OpenAI
    OPENAI_API_KEY: str

    # 🧠 Qdrant
    QDRANT_URL: str
    QDRANT_API_KEY: str

    # 🗄️ Database
    DATABASE_URL: str

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore"  # ← temporarily ignore extra fields for testing
    )

settings = Settings()


class TokenData(BaseModel):
    user_id: str
    exp: Optional[datetime] = None


# Try to use bcrypt, fallback to pbkdf2 if bcrypt fails
try:
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def verify_password(plain_password: str, hashed_password: str) -> bool:
        return pwd_context.verify(plain_password, hashed_password)

    def get_password_hash(password: str) -> str:
        # Bcrypt has a 72-byte password length limit
        # Truncate password if it exceeds the limit
        if len(password.encode('utf-8')) > 72:
            password = password.encode('utf-8')[:72].decode('utf-8', errors='ignore')
        return pwd_context.hash(password)
except Exception:
    # Fallback to pbkdf2 if bcrypt is not available or has issues
    from passlib.context import CryptContext
    pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")

    def verify_password(plain_password: str, hashed_password: str) -> bool:
        return pwd_context.verify(plain_password, hashed_password)

    def get_password_hash(password: str) -> str:
        return pwd_context.hash(password)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt


def verify_token(token: str) -> Optional[TokenData]:
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            return None
        token_data = TokenData(user_id=user_id, exp=datetime.fromtimestamp(payload.get("exp")))
        return token_data
    except jwt.JWTError:
        return None