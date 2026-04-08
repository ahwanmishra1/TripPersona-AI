from src.tools.weather import get_weather
from src.tools.places import get_places
from src.tools.budget import get_budget_breakdown
from src.services.personality_service import transform_plan


def normalize_input_node(state: dict) -> dict:
    return {
        **state,
        "request": state["request"],
    }


def gather_context_node(state: dict) -> dict:
    req = state["request"]
    context = {
        "weather": get_weather(req["destination"]),
        "places": get_places(req["destination"]),
        "budget": get_budget_breakdown(req["days"], req["people"], req["budget_inr"]),
    }
    return {**state, "context": context}


def generate_base_plan_node(state: dict) -> dict:
    req = state["request"]
    place_data = state["context"]["places"]
    budget = state["context"]["budget"]

    popular_places = place_data["popular_places"]
    food_areas = place_data["food_areas"]

    itinerary = []
    for i in range(req["days"]):
        p1 = popular_places[i % len(popular_places)]
        p2 = popular_places[(i + 1) % len(popular_places)]
        food_stop = food_areas[i % len(food_areas)]

        itinerary.append(
            {
                "day": i + 1,
                "morning": f"Visit {p1}",
                "afternoon": f"Explore {p2} and break for lunch around {food_stop}",
                "evening": f"Relaxed dinner and a nearby walk around {food_stop}",
                "estimated_cost_inr": max(1200, budget["total"] // req["days"]),
            }
        )

    base_plan = {
        "summary": f"{req['days']}-day trip from {req['source']} to {req['destination']} for {req['people']} people.",
        "itinerary": itinerary,
        "budget": budget,
        "stay_areas": place_data["stay_areas"],
        "signature_foods": place_data["signature_foods"],
    }

    return {**state, "base_plan": base_plan}


def apply_personalities_node(state: dict) -> dict:
    base_plan = state["base_plan"]
    context = state["context"]
    request = state["request"]

    personalities = {
        "planner": transform_plan(base_plan, "planner", context, request),
        "chaotic": transform_plan(base_plan, "chaotic", context, request),
        "local": transform_plan(base_plan, "local", context, request),
        "foodie": transform_plan(base_plan, "foodie", context, request),
    }
    return {**state, "personalities": personalities}


def format_response_node(state: dict) -> dict:
    req = state["request"]
    response = {
        "trip_summary": {
            "source": req["source"],
            "destination": req["destination"],
            "days": req["days"],
            "people": req["people"],
            "budget_inr": req["budget_inr"],
            "preferences": req.get("preferences", ""),
        },
        "context": state["context"],
        "base_plan": state["base_plan"],
        "personalities": state["personalities"],
    }
    return {**state, "response": response}