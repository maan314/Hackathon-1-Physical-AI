from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


class HardwareComponent(BaseModel):
    id: str
    name: str
    description: str
    category: str  # sensors, actuators, processors, etc.
    manufacturer: str
    model: str
    specifications: dict
    price: Optional[float] = None
    availability: str  # cloud, on-prem, both
    sim_to_real_latency: Optional[float] = None  # in milliseconds
    sim_to_real_accuracy: Optional[float] = None  # percentage


class HardwareSetup(BaseModel):
    id: str
    name: str
    description: str
    components: List[str]  # list of component IDs
    difficulty_level: str  # beginner, intermediate, advanced
    estimated_cost: Optional[float] = None
    estimated_time: str  # e.g., "2-4 weeks"
    lab_path: str  # cloud or on-prem
    sim_to_real_considerations: List[str]


class HardwareLab(BaseModel):
    id: str
    name: str
    description: str
    setup_id: str
    requirements: List[str]
    safety_considerations: List[str]
    cloud_vs_on_prem_comparison: dict
    latency_warnings: List[str]
    sim_to_real_warnings: List[str]
    created_at: datetime
    updated_at: datetime


class HardwareRecommendation(BaseModel):
    id: str
    component_id: str
    use_case: str
    recommendation_type: str  # essential, recommended, optional
    justification: str
    alternative_options: List[str]
    created_at: datetime

    class Config:
        from_attributes = True