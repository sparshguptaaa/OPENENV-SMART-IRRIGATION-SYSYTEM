import os
import requests
from openai import OpenAI

API_BASE_URL = os.environ["API_BASE_URL"]
API_KEY = os.environ.get("API_KEY")

client = OpenAI(
    base_url=API_BASE_URL,
    api_key=API_KEY
)


def run():
    print("[START] task=irrigation", flush=True)

    
    try:
        client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": "Hello"}],
            max_tokens=5
        )
    except Exception:
        pass  

    try:
        res = requests.post(f"{API_BASE_URL}/reset", params={"difficulty": "easy"})
        data = res.json()
        obs = data["observation"]
    except Exception:
        print("[END] task=irrigation score=0 steps=0", flush=True)
        return

    total_reward = 0
    step_count = 0

    for step in range(1, 11):
        try:
            moisture = obs["soil_moisture"]

            if moisture < 0.3:
                action = "irrigate_high"
            elif moisture < 0.4:
                action = "irrigate_low"
            else:
                action = "wait"

            res = requests.post(
                f"{API_BASE_URL}/step",
                json={"action": {"action_type": action}}
            )

            data = res.json()
            obs = data["observation"]
            reward = data["reward"]
            done = data["done"]

        except Exception:
            break

        total_reward += reward
        step_count += 1

        print(f"[STEP] step={step} reward={reward}", flush=True)

        if done:
            break

    score = total_reward / step_count if step_count > 0 else 0

    print(f"[END] task=irrigation score={score} steps={step_count}", flush=True)


if __name__ == "__main__":
    run()
