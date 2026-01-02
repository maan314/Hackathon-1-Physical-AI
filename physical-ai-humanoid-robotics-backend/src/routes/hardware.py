from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.services.hardware_service import HardwareService
from src.models.hardware import HardwareComponent, HardwareSetup, HardwareLab, HardwareRecommendation
from src.database.database import get_db
from src.routes.auth import get_current_user


router = APIRouter()


@router.get("/components", response_model=list)
async def get_hardware_components(db: AsyncSession = Depends(get_db)):
    hardware_service = HardwareService(db)
    return await hardware_service.get_hardware_components()


@router.get("/setups", response_model=list)
async def get_hardware_setups(db: AsyncSession = Depends(get_db)):
    hardware_service = HardwareService(db)
    return await hardware_service.get_hardware_setups()


@router.get("/labs", response_model=list)
async def get_hardware_labs(db: AsyncSession = Depends(get_db)):
    hardware_service = HardwareService(db)
    return await hardware_service.get_hardware_labs()


@router.get("/recommendations", response_model=list)
async def get_hardware_recommendations(
    user_experience: str = "beginner",
    current_user=Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    hardware_service = HardwareService(db)
    return await hardware_service.get_hardware_recommendations(user_experience)


@router.get("/cloud-vs-on-prem", response_model=dict)
async def get_cloud_vs_on_prem_comparison(db: AsyncSession = Depends(get_db)):
    hardware_service = HardwareService(db)
    return await hardware_service.get_cloud_vs_on_prem_comparison()


@router.get("/latency-considerations", response_model=list)
async def get_latency_considerations(db: AsyncSession = Depends(get_db)):
    hardware_service = HardwareService(db)
    return await hardware_service.get_latency_considerations()


@router.get("/sim-to-real-warnings", response_model=list)
async def get_sim_to_real_warnings(db: AsyncSession = Depends(get_db)):
    hardware_service = HardwareService(db)
    return await hardware_service.get_sim_to_real_warnings()