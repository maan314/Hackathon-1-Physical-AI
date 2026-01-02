from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.services.personalization_service import PersonalizationService
from src.models.personalization import (
    PersonalizationProfileCreate, PersonalizationProfileUpdate,
    PersonalizationProfile, ContentPersonalization, PersonalizationRecommendation
)
from src.database.database import get_db
from src.routes.auth import get_current_user


router = APIRouter()


@router.post("/profiles", response_model=PersonalizationProfile)
async def create_or_update_profile(
    profile_data: PersonalizationProfileCreate,
    current_user=Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    personalization_service = PersonalizationService(db)
    return await personalization_service.create_or_update_profile(profile_data)


@router.get("/profiles", response_model=PersonalizationProfile)
async def get_profile(
    current_user=Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    personalization_service = PersonalizationService(db)
    profile = await personalization_service.get_profile(current_user.user_id)

    if not profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Profile not found"
        )

    return profile


@router.put("/profiles", response_model=PersonalizationProfile)
async def update_profile(
    profile_update: PersonalizationProfileUpdate,
    current_user=Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    personalization_service = PersonalizationService(db)
    updated_profile = await personalization_service.update_profile(current_user.user_id, profile_update)

    if not updated_profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Profile not found"
        )

    return updated_profile


@router.get("/content/{content_id}/personalized", response_model=ContentPersonalization)
async def get_personalized_content(
    content_id: str,
    current_user=Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    personalization_service = PersonalizationService(db)
    personalized_content = await personalization_service.get_personalized_content(current_user.user_id, content_id)

    if not personalized_content:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Personalized content not found"
        )

    return personalized_content


@router.get("/recommendations", response_model=list)
async def get_recommendations(
    current_user=Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    personalization_service = PersonalizationService(db)
    return await personalization_service.get_recommendations(current_user.user_id)


@router.get("/learning-path", response_model=list)
async def get_personalized_learning_path(
    current_user=Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    personalization_service = PersonalizationService(db)
    return await personalization_service.get_personalized_learning_path(current_user.user_id)