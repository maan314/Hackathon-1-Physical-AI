from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.services.progress_service import ProgressService
from src.models.progress import ProgressCreate, ProgressUpdate, UserProgress, QuizAttempt, LearningPath
from src.database.database import get_db
from src.routes.auth import get_current_user


router = APIRouter()


@router.post("/progress", response_model=UserProgress)
async def create_or_update_progress(
    progress_data: ProgressCreate,
    current_user=Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    progress_service = ProgressService(db)
    return await progress_service.create_or_update_progress(progress_data)


@router.get("/progress/{content_id}", response_model=UserProgress)
async def get_user_progress(
    content_id: str,
    current_user=Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    progress_service = ProgressService(db)
    user_progress = await progress_service.get_user_progress(current_user.user_id, content_id)

    if not user_progress:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Progress not found"
        )

    return user_progress


@router.get("/progress/", response_model=list)
async def get_user_all_progress(
    current_user=Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    progress_service = ProgressService(db)
    return await progress_service.get_user_all_progress(current_user.user_id)


@router.put("/progress/{content_id}", response_model=UserProgress)
async def update_progress(
    content_id: str,
    progress_update: ProgressUpdate,
    current_user=Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    progress_service = ProgressService(db)
    updated_progress = await progress_service.update_progress(current_user.user_id, content_id, progress_update)

    if not updated_progress:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Progress not found"
        )

    return updated_progress


@router.get("/stats/", response_model=dict)
async def get_user_completion_stats(
    current_user=Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    progress_service = ProgressService(db)
    return await progress_service.get_user_completion_stats(current_user.user_id)


@router.post("/quiz-attempts", response_model=QuizAttempt)
async def create_quiz_attempt(
    content_id: str,
    score: float,
    total_questions: int,
    correct_answers: int,
    time_taken: int,
    current_user=Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    progress_service = ProgressService(db)
    return await progress_service.create_quiz_attempt(
        current_user.user_id,
        content_id,
        score,
        total_questions,
        correct_answers,
        time_taken
    )


@router.get("/quiz-attempts/{content_id}", response_model=list)
async def get_user_quiz_attempts(
    content_id: str,
    current_user=Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    progress_service = ProgressService(db)
    return await progress_service.get_user_quiz_attempts(current_user.user_id, content_id)


@router.post("/learning-paths", response_model=LearningPath)
async def create_learning_path(
    name: str,
    description: str,
    content_ids: list,
    current_user=Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    progress_service = ProgressService(db)
    return await progress_service.create_learning_path(current_user.user_id, name, description, content_ids)


@router.get("/learning-paths/", response_model=list)
async def get_user_learning_paths(
    current_user=Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    progress_service = ProgressService(db)
    return await progress_service.get_user_learning_paths(current_user.user_id)


@router.get("/learning-paths/{path_id}", response_model=LearningPath)
async def get_learning_path(
    path_id: str,
    current_user=Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    progress_service = ProgressService(db)
    path = await progress_service.get_learning_path(path_id)

    if not path or path.user_id != current_user.user_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Learning path not found"
        )

    return path


@router.put("/learning-paths/{path_id}", response_model=LearningPath)
async def update_learning_path(
    path_id: str,
    name: str = None,
    description: str = None,
    content_ids: list = None,
    current_user=Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    progress_service = ProgressService(db)
    updated_path = await progress_service.update_learning_path(path_id, name, description, content_ids)

    if not updated_path or updated_path.user_id != current_user.user_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Learning path not found"
        )

    return updated_path


@router.delete("/learning-paths/{path_id}")
async def delete_learning_path(
    path_id: str,
    current_user=Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    progress_service = ProgressService(db)
    success = await progress_service.delete_learning_path(path_id)

    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Learning path not found"
        )

    return {"message": "Learning path deleted successfully"}