from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.services.translation_service import TranslationService
from src.models.translation import TranslationRequestCreate, TranslationRequest, SupportedLanguage
from src.database.database import get_db
from src.routes.auth import get_current_user


router = APIRouter()


@router.post("/requests", response_model=TranslationRequest)
async def request_translation(
    translation_data: TranslationRequestCreate,
    current_user=Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    translation_service = TranslationService(db)
    return await translation_service.request_translation(translation_data, current_user.user_id)


@router.get("/requests/{request_id}", response_model=TranslationRequest)
async def get_translation_request(
    request_id: str,
    current_user=Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    translation_service = TranslationService(db)
    request = await translation_service.get_translation_request(request_id)

    if not request or (request.user_id and request.user_id != current_user.user_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Translation request not found"
        )

    return request


@router.get("/languages", response_model=list)
async def get_supported_languages(db: AsyncSession = Depends(get_db)):
    translation_service = TranslationService(db)
    return await translation_service.get_supported_languages()


@router.post("/translate", response_model=str)
async def translate_content_directly(
    content: str,
    source_lang: str = "en",
    target_lang: str = "ur",
    preserve_formatting: bool = True,
    current_user=Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    translation_service = TranslationService(db)
    return await translation_service.translate_content(content, source_lang, target_lang, preserve_formatting)