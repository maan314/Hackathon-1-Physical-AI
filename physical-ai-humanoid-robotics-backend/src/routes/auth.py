from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession

from src.services.auth_service import AuthService
from src.models.auth import LoginRequest, RegisterRequest, TokenResponse, UserProfile
from src.models.user import UserCreate, UserUpdate
from src.database.database import get_db
from src.utils.security import verify_token, TokenData


router = APIRouter()
security = HTTPBearer()


async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)) -> TokenData:
    token_data = verify_token(credentials.credentials)
    if not token_data:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return token_data


@router.post("/register", response_model=UserProfile)
async def register(user_data: RegisterRequest, db: AsyncSession = Depends(get_db)):
    auth_service = AuthService(db)
    # Convert RegisterRequest to UserCreate, handling enum fields properly
    user_create_data = UserCreate(
        email=user_data.email,
        password=user_data.password,
        name=user_data.name,
        software_experience=user_data.software_experience,
        hardware_experience=user_data.hardware_experience
    )
    return await auth_service.register_user(user_create_data)


@router.post("/login", response_model=TokenResponse)
async def login(login_data: LoginRequest, db: AsyncSession = Depends(get_db)):
    auth_service = AuthService(db)
    token_response = await auth_service.authenticate_user(login_data.email, login_data.password)

    if not token_response:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return token_response


@router.get("/profile", response_model=UserProfile)
async def get_profile(current_user: TokenData = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    auth_service = AuthService(db)
    profile = await auth_service.get_user_profile(current_user.user_id)

    if not profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    return profile


@router.put("/profile", response_model=UserProfile)
async def update_profile(
    user_update: UserUpdate,
    current_user: TokenData = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    auth_service = AuthService(db)
    profile = await auth_service.update_user_profile(current_user.user_id, user_update)

    if not profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    return profile