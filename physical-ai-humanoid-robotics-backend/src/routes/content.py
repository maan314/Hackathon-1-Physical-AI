from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.services.content_service import ContentService
from src.models.content import ContentCreate, ContentUpdate, Content, Module, Chapter
from src.database.database import get_db
from src.routes.auth import get_current_user


router = APIRouter()


@router.post("/", response_model=Content)
async def create_content(
    content_data: ContentCreate,
    current_user=Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    content_service = ContentService(db)
    return await content_service.create_content(content_data)


@router.get("/{content_id}", response_model=Content)
async def get_content(content_id: str, db: AsyncSession = Depends(get_db)):
    content_service = ContentService(db)
    content = await content_service.get_content(content_id)

    if not content:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Content not found"
        )

    return content


@router.get("/module/{module_type}", response_model=list)
async def get_content_by_module_type(module_type: str, db: AsyncSession = Depends(get_db)):
    content_service = ContentService(db)
    contents = await content_service.get_content_by_module_type(module_type)
    return contents


@router.put("/{content_id}", response_model=Content)
async def update_content(
    content_id: str,
    content_update: ContentUpdate,
    current_user=Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    content_service = ContentService(db)
    content = await content_service.update_content(content_id, content_update)

    if not content:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Content not found"
        )

    return content


@router.delete("/{content_id}")
async def delete_content(
    content_id: str,
    current_user=Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    content_service = ContentService(db)
    success = await content_service.delete_content(content_id)

    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Content not found"
        )

    return {"message": "Content deleted successfully"}


@router.get("/modules/", response_model=list)
async def get_modules(db: AsyncSession = Depends(get_db)):
    content_service = ContentService(db)
    return await content_service.get_modules()


@router.get("/modules/{module_id}/chapters", response_model=list)
async def get_chapters_by_module(module_id: str, db: AsyncSession = Depends(get_db)):
    content_service = ContentService(db)
    return await content_service.get_chapters_by_module(module_id)