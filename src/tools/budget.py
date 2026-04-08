def get_budget_breakdown(days: int, people: int, budget_inr: int) -> dict:
    stay = int(budget_inr * 0.35)
    travel = int(budget_inr * 0.25)
    food = int(budget_inr * 0.20)
    activities = budget_inr - stay - travel - food

    return {
        "total": budget_inr,
        "per_person": budget_inr // people,
        "stay": stay,
        "travel": travel,
        "food": food,
        "activities": activities,
        "days": days,
        "people": people,
    }