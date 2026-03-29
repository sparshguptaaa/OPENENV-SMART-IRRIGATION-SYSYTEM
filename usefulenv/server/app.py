from fastapi import FastAPI
from server.environment import UsefulEnv

app = FastAPI()
env = UsefulEnv()


@app.post("/reset")
def reset(difficulty: str = "easy"):
    return env.reset(difficulty=difficulty)


@app.post("/step")
def step(action: dict):
    action_type = action.get("action", {}).get("action_type", "wait")

    result = env.step(type("obj", (), {"action_type": action_type}))

    return {
        "observation": {
            "soil_moisture": result.soil_moisture,
            "crop_health": result.crop_health,
            "water_available": result.water_available,
            "message": result.message,
        },
        "reward": result.reward,
        "done": result.done,
    }
def main():
    import uvicorn
    uvicorn.run("server.app:app", host="0.0.0.0", port=8000)


if __name__ == "__main__":
    main()
