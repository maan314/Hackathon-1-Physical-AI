from fastapi import APIRouter, Depends, UploadFile, File, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional

from src.services.content_service import ContentService
from src.models.content import ContentCreate
from src.database.database import get_db
from src.routes.auth import get_current_user

router = APIRouter()


@router.post("/ingest", status_code=status.HTTP_201_CREATED)
async def ingest_document(
    file: UploadFile = File(...),
    current_user=Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Ingest a document for RAG processing
    """
    content_service = ContentService(db)

    # Validate file type
    allowed_types = ["application/pdf", "text/plain", "text/markdown", "application/msword",
                     "application/vnd.openxmlformats-officedocument.wordprocessingml.document"]

    if file.content_type not in allowed_types:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"File type {file.content_type} not supported. Allowed types: {allowed_types}"
        )

    # Read file content
    content = await file.read()
    content_str = content.decode('utf-8') if isinstance(content, bytes) else str(content)

    # Create content object
    content_data = ContentCreate(
        title=file.filename,
        content=content_str,
        content_type=file.content_type,
        source="upload",
        module_type="document"
    )

    # Store in database
    created_content = await content_service.create_content(content_data)

    return {
        "message": "Document ingested successfully",
        "document_id": created_content.id,
        "filename": file.filename,
        "size": len(content_str)
    }


@router.post("/ingest/text", status_code=status.HTTP_201_CREATED)
async def ingest_text(
    content_data: ContentCreate,
    current_user=Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Ingest text content for RAG processing
    """
    content_service = ContentService(db)

    # Store in database
    created_content = await content_service.create_content(content_data)

    return {
        "message": "Text content ingested successfully",
        "content_id": created_content.id,
        "title": created_content.title
    }