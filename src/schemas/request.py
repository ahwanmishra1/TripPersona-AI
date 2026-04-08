from pydantic import BaseModel, Field


class TripRequest(BaseModel):
    source: str = Field(..., min_length=1)
    destination: str = Field(..., min_length=1)
    days: int = Field(..., ge=1, le=14)
    people: int = Field(..., ge=1, le=20)
    budget_inr: int = Field(..., ge=1000)
    preferences: str = ""