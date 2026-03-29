from typing import List, Dict


def grade(history: List[Dict]) -> float:


    if not history:
        return 0.0

    total_reward = 0.0
    total_health = 0.0
    steps = len(history)

    for step in history:
        total_reward += step.get("reward", 0.0)
        total_health += step.get("health", 0.0)

    # Average metrics
    avg_reward = total_reward / steps
    avg_health = total_health / steps

   
    normalized_reward = (avg_reward + 2) / 4
    
    normalized_reward = max(min(normalized_reward, 1.0), 0.0)

   
    normalized_health = max(min(avg_health, 1.0), 0.0)

    # Final score (weighted)
    score = 0.6 * normalized_reward + 0.4 * normalized_health

    return round(score, 4)