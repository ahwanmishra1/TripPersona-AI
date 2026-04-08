from typing import TypedDict, Any


class TripState(TypedDict, total=False):
    request: dict[str, Any]
    context: dict[str, Any]
    base_plan: dict[str, Any]
    personalities: dict[str, Any]
    response: dict[str, Any]