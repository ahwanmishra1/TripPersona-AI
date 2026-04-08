from pydantic import BaseModel
from typing import Any


class PersonalityPlan(BaseModel):
    title: str
    vibe: str
    summary: str
    itinerary: list[dict[str, Any]]
    stay: list[str]
    food: list[str]
    tips: list[str]


class TripResponse(BaseModel):
    trip_summary: dict[str, Any]
    context: dict[str, Any]
    base_plan: dict[str, Any]
    personalities: dict[str, PersonalityPlan]