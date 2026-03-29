import random
import uuid

from models import IrrigationAction, IrrigationObservation, IrrigationState,Difficulty


class UsefulEnv:
    SUPPORTS_CONCURRENT_SESSIONS = True

    MAX_STEPS = 15

    def __init__(self):
        self._state = IrrigationState()
        self._soil_moisture = 0.5
        self._crop_health = 0.8
        self._water_available = 10
        self._history = []


    def reset(self, seed=None, episode_id=None, difficulty: Difficulty = Difficulty.easy, **kwargs) -> IrrigationObservation:
        if seed is not None:
            random.seed(seed)

        if difficulty == Difficulty.easy:
            self._soil_moisture = 0.5
            self._water_available = 10
        elif difficulty == Difficulty.medium:
            self._soil_moisture = 0.4
            self._water_available = 7
        else:
            self._soil_moisture = 0.3
            self._water_available = 5

        self._crop_health = 0.8

        self._state = IrrigationState(
            episode_id=episode_id or str(uuid.uuid4()),
            step_count=0,
            max_steps=self.MAX_STEPS
            
        )
        self._state.difficulty = difficulty

        return {
            "done": False,
            "reward": None,
            "soil_moisture": self._soil_moisture,
            "crop_health": self._crop_health,
            "water_available": self._water_available,
            "message": "Irrigation started. Maintain optimal soil moisture (0.4 - 0.7)."
}

  
    def step(self, action: IrrigationAction, timeout_s=None, **kwargs) -> IrrigationObservation:
        message = ""
        action_type = action.action_type
        self._state.step_count += 1
        reward = 0

        if action_type == "irrigate_low" and self._water_available >= 1:
            self._soil_moisture += 0.2
            self._water_available -= 1
            reward-=0.1 #  water usge penalty

        elif action_type == "irrigate_high" and self._water_available >= 2:
            self._soil_moisture += 0.4
            self._water_available -= 2
            reward-=0.2 # high water usage penalty

        elif action_type == "wait":
            pass

        else:
            reward -= 0.5  # invalid or no water

       
        # Environment dynamics
       
        self._soil_moisture -= 0.1  # drying

        # Random rain
        if random.random() < 0.3:
            self._soil_moisture += 0.3

        # Clamp values
        self._soil_moisture = max(min(self._soil_moisture, 1.0), 0.0)

        if 0.4 <= self._soil_moisture <= 0.7:
            self._crop_health += 0.1
            reward += 1
            message = "Optimal moisture. Crop growing well "
        else:
            self._crop_health -= 0.1
            reward -= 1
            message = "Bad moisture level. Crop stressed "

        # Over-irrigation penalty
        if self._soil_moisture > 0.8:
            reward -= 0.5
            message += " Over-irrigation!"

        # Time penalty
        reward -= 0.05 * self._state.step_count

        # Clamp crop health
        self._crop_health = max(min(self._crop_health, 1.0), 0.0)

        if action_type in ["irrigate_low", "irrigate_high"]:
            reward -= 0.1
            message+=" water usage penalty"  # water usage penalty

       
        done = (
            self._state.step_count >= self.MAX_STEPS or
            self._crop_health <= 0
        )

        if done:
            if self._crop_health > 0:
                message = "Episode completed successfully ✅"
                reward += 1
            else:
                message = "Crop failed ❌"
                reward -= 1

        self._history.append({
                "moisture": self._soil_moisture,
                "action": action_type,
                "reward": reward
        })        

        return IrrigationObservation(
            done=done,
            reward=reward,
            soil_moisture=self._soil_moisture,
            crop_health=self._crop_health,
            water_available=self._water_available,
            message=message
        )
    @property
    def state(self) -> IrrigationState:
        return self._state
    
    def get_history(self):
        return self._history