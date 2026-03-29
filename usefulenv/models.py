from typing import Optional
from pydantic import BaseModel


class IrrigationAction(BaseModel):
    action_type: str


class IrrigationObservation(BaseModel):
    done: bool
    reward: Optional[float] = None
    soil_moisture: float
    crop_health: float
    water_available: int
    message: str


class IrrigationState(BaseModel):
    episode_id: Optional[str] = None
    step_count: int = 0
    max_steps: int = 15
    difficulty:str='easy'
    


class Difficulty:
    easy = "easy"
    medium = "medium"
    hard = "hard"