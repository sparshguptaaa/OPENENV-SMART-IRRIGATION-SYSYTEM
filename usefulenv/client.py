from openenv.core.env_client import EnvClient
from openenv.core.client_types import StepResult
from models import IrrigationAction, IrrigationObservation, IrrigationState, Difficulty


class UsefulEnvClient(EnvClient[IrrigationAction, IrrigationObservation, IrrigationState]):

    def __init__(self, base_url: str = "http://localhost:8000"):
        super().__init__(base_url=base_url)

    
    # SEND ACTION
   
    def _step_payload(self, action: IrrigationAction) -> dict:
        return {
            "action_type": action.action_type
        }

    
    # PARSE STEP RESULT
    
    def _parse_result(self, payload: dict) -> StepResult:
        obs_data = payload.get("observation", {})

        return StepResult(
            observation=IrrigationObservation(
                done=payload.get("done", False),
                reward=payload.get("reward"),
                soil_moisture=obs_data.get("soil_moisture", 0.0),
                crop_health=obs_data.get("crop_health", 0.0),
                water_available=obs_data.get("water_available", 0),
                message=obs_data.get("message", ""),
            ),
            reward=payload.get("reward"),
            done=payload.get("done", False),
        )

    # PARSE STATE
    def _parse_state(self, payload: dict) -> IrrigationState:
        return IrrigationState(
            episode_id=payload.get("episode_id"),
            step_count=payload.get("step_count", 0),
            max_steps=payload.get("max_steps", 15),
            difficulty=Difficulty(payload.get("difficulty")) if payload.get("difficulty") else None
        )

    # OPTIONAL RESET WRAPPER
    def reset(self, difficulty="easy"):
        return super().reset(params={"difficulty": difficulty})