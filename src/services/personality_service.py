import json
from src.llm.loader import get_llm


FALLBACK_PERSONALITIES = {
    "planner": {
        "title": "The Planner",
        "vibe": "Structured, efficient, practical",
        "summary": "A balanced trip with clear pacing, efficient movement, and budget visibility.",
    },
    "chaotic": {
        "title": "The Chaotic Friend",
        "vibe": "Spontaneous, fun, energetic",
        "summary": "A looser trip with room for detours, surprises, and impulsive fun.",
    },
    "local": {
        "title": "The Local Insider",
        "vibe": "Authentic, cultural, less touristy",
        "summary": "A grounded trip focused on local flavor, hidden gems, and authentic experiences.",
    },
    "foodie": {
        "title": "The Foodie Traveller",
        "vibe": "Flavor-first, indulgent, sensory, memorable",
        "summary": "A trip designed around unforgettable meals, local specialties, cafés, markets, and culinary moments.",
    },
}


def fallback_transform(base_plan: dict, personality: str, context: dict) -> dict:
    info = FALLBACK_PERSONALITIES[personality]
    itinerary = base_plan["itinerary"]

    place_data = context.get("places", {})
    stay_areas = place_data.get("stay_areas", ["city center"])
    food_areas = place_data.get("food_areas", ["local dining district"])
    signature_foods = place_data.get("signature_foods", ["regional specialty"])
    local_places = place_data.get("local_places", ["hidden neighborhood spot"])

    if personality == "planner":
        mod_itinerary = [
            {
                **day,
                "morning": f"{day['morning']} early to avoid crowds",
                "afternoon": f"{day['afternoon']} with a pre-planned meal stop",
                "evening": "Dinner near your stay and wind down early",
            }
            for day in itinerary
        ]
        stay = [
            f"Stay around {stay_areas[0]} for convenience and clean connectivity",
            f"{stay_areas[1] if len(stay_areas) > 1 else stay_areas[0]} works well for efficient daily movement",
        ]
        food = [
            f"Plan dependable meals around {food_areas[0]}",
            f"Prioritize one signature dish like {signature_foods[0]}",
        ]
        tips = [
            "Start early",
            "Pre-book major attractions",
            "Track daily spend and commute time",
        ]

    elif personality == "chaotic":
        mod_itinerary = [
            {
                **day,
                "evening": f"{day['evening']} plus a spontaneous stop if the vibe feels right",
            }
            for day in itinerary
        ]
        stay = [
            f"Stay somewhere lively like {stay_areas[0]}",
            "Choose a flexible booking in a high-energy neighborhood",
        ]
        food = [
            f"Mix street food around {food_areas[0]} with random café discoveries",
            f"Do not miss a bold local bite like {signature_foods[0]}",
        ]
        tips = [
            "Keep one slot free daily",
            "Say yes to one random detour",
            "Avoid over-planning mornings",
        ]

    elif personality == "foodie":
        mod_itinerary = [
            {
                **day,
                "morning": f"Start with coffee or breakfast around {food_areas[i % len(food_areas)]}",
                "afternoon": f"{day['afternoon']} but centered around tasting {signature_foods[i % len(signature_foods)]}",
                "evening": f"Make dinner the highlight of the day around {food_areas[i % len(food_areas)]}",
            }
            for i, day in enumerate(itinerary)
        ]
        stay = [
            f"Stay near {stay_areas[0]} for easy access to food spots",
            f"{stay_areas[1] if len(stay_areas) > 1 else stay_areas[0]} is ideal for café and dinner hopping",
        ]
        food = [
            f"Prioritize {signature_foods[0]}",
            f"Explore dining around {food_areas[0]}",
            f"Leave room for dessert, snacks, and one standout dinner around {food_areas[1] if len(food_areas) > 1 else food_areas[0]}",
        ]
        tips = [
            "Plan your day around meal windows",
            "Keep one unplanned stop for a surprise food find",
            "Balance iconic dishes with neighborhood favorites",
        ]

    else:
        mod_itinerary = [
            {
                **day,
                "morning": f"Begin in {local_places[i % len(local_places)]}",
                "afternoon": f"Explore a quieter local pocket near {local_places[i % len(local_places)]} and eat somewhere unflashy but loved",
                "evening": "Slow walk, regional food, and neighborhood people-watching",
            }
            for i, day in enumerate(itinerary)
        ]
        stay = [
            f"Stay near a more lived-in area like {stay_areas[-1]}",
            "Prefer a boutique stay or homestay feel over a generic chain",
        ]
        food = [
            f"Try smaller places serving {signature_foods[0]}",
            f"Look around {food_areas[-1]} for less touristy food stops",
        ]
        tips = [
            "Go beyond the obvious landmarks",
            "Spend time in neighborhoods",
            "Let slower local moments shape the day",
        ]

    return {
        "title": info["title"],
        "vibe": info["vibe"],
        "summary": info["summary"],
        "itinerary": mod_itinerary,
        "stay": stay,
        "food": food,
        "tips": tips,
    }


def llm_transform(base_plan: dict, personality: str, context: dict, request: dict) -> dict:
    llm = get_llm()
    if llm is None:
        return fallback_transform(base_plan, personality, context)

    personality_instructions = {
        "planner": """
You are The Planner.
Rewrite the trip as an organized, efficient, realistic itinerary.
Optimize pacing, reduce wasted movement, and keep budget visibility.
Tone: smart, calm, structured.
""",
        "chaotic": """
You are The Chaotic Friend.
Rewrite the trip as spontaneous, exciting, high-energy, slightly impulsive, and memorable.
Add playful detours, fun moments, bold food choices, and lively evening energy.
Tone: witty, exciting, playful.
""",
        "local": """
You are The Local Insider.
Rewrite the trip like someone who actually knows the place deeply.
Prefer hidden gems, neighborhood charm, authentic food, and less touristy experiences.
Tone: warm, insider, cultural, grounded.
""",
        "foodie": """
You are The Foodie Traveller.
Rewrite the trip around unforgettable food experiences.
Prioritize iconic local dishes, markets, cafés, desserts, food streets, and one standout dining moment.
Food should drive the itinerary.
Tone: rich, descriptive, indulgent, classy.
""",
    }

    prompt = f"""
{personality_instructions[personality]}

Trip request:
{json.dumps(request, indent=2)}

Context:
{json.dumps(context, indent=2)}

Base plan:
{json.dumps(base_plan, indent=2)}

Return ONLY valid JSON with this exact shape:
{{
  "title": "string",
  "vibe": "string",
  "summary": "string",
  "itinerary": [
    {{
      "day": 1,
      "morning": "string",
      "afternoon": "string",
      "evening": "string",
      "estimated_cost_inr": 1000
    }}
  ],
  "stay": ["string"],
  "food": ["string"],
  "tips": ["string"]
}}

Rules:
- Keep the number of days exactly the same.
- Keep costs in INR.
- Use destination-specific context from the provided places data.
- Stay suggestions must reference real stay areas when available.
- Food suggestions must reference signature foods or food areas when available.
- Do not output markdown.
- Do not wrap JSON in backticks.
"""

    try:
        raw = llm.invoke(prompt)
        content = raw.content if hasattr(raw, "content") else str(raw)
        return json.loads(content)
    except Exception:
        return fallback_transform(base_plan, personality, context)


def transform_plan(base_plan: dict, personality: str, context: dict | None = None, request: dict | None = None) -> dict:
    context = context or {}
    request = request or {}
    return llm_transform(base_plan, personality, context, request)