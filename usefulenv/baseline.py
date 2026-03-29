import requests
from models import Difficulty
from server.grader import grade


BASE_URL = "http://127.0.0.1:8000"


def run_baseline():
    # RESET
    res = requests.post(f"{BASE_URL}/reset", params={"difficulty": Difficulty.medium})
    obs = res.json()

    done = obs.get("done", False)

    history = []

    while not done:
        moisture = obs["soil_moisture"]

        if moisture < 0.35:
            action_type = "irrigate_high"
        elif moisture < 0.5:
            action_type = "irrigate_low"
        elif 0.5 <= moisture <= 0.7:
            action_type = "wait"
        else:
            action_type = "wait"

        # STEP
        res = requests.post(
            f"{BASE_URL}/step",
            json={"action": {"action_type": action_type}}
        )

        data = res.json()

        obs = data["observation"]
        done = data["done"]

        history.append({
            "reward": data["reward"],
            "health": obs["crop_health"]
        })

    # FINAL SCORE
    score = grade(history)
    return score


if __name__ == "__main__":
    final_score = run_baseline()
    print(f"Baseline Score: {final_score}")