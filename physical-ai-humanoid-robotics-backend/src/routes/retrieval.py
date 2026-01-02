from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional, List, Dict, Any

from src.services.content_service import ContentService
from src.models.content import Content
from src.database.database import get_db
from src.routes.auth import get_current_user

router = APIRouter()


@router.post("/retrieve", response_model=List[Dict[str, Any]])
async def retrieve_content(
    query: str,
    top_k: Optional[int] = 5,
    filters: Optional[Dict[str, Any]] = None,
    current_user=Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Retrieve relevant content based on query for RAG
    """
    if not query or len(query.strip()) == 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Query cannot be empty"
        )

    content_service = ContentService(db)

    # Retrieve relevant content based on query
    # This is a simplified implementation - in a real RAG system, this would involve
    # semantic search using vector databases like Qdrant
    retrieved_content = await content_service.search_content(query, top_k=top_k, filters=filters)

    return retrieved_content


@router.get("/retrieve/{content_id}", response_model=Dict[str, Any])
async def get_content_by_id(
    content_id: str,
    current_user=Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Retrieve specific content by ID
    """
    content_service = ContentService(db)

    content = await content_service.get_content(content_id)

    if not content:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Content not found"
        )

    return {
        "id": content.id,
        "title": content.title,
        "content": content.content,
        "content_type": content.content_type,
        "created_at": content.created_at,
        "updated_at": content.updated_at
    }


@router.get("/retrieve/module/{module_type}", response_model=List[Dict[str, Any]])
async def get_content_by_module(
    module_type: str,
    current_user=Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Retrieve content by module type
    """
    content_service = ContentService(db)

    content_list = await content_service.get_content_by_module_type(module_type)

    return content_list