"""Pydantic request schemas for /api/v1/ngos/*, per §4."""
from datetime import datetime

from pydantic import BaseModel


class UpdateNGOProfileRequest(BaseModel):
    organisation_name: str | None = None
    address: str | None = None
    latitude: float | None = None
    longitude: float | None = None
    operating_start: str | None = None
    operating_end: str | None = None
    accepted_categories: list[str] | None = None


class UpdateDemandRequest(BaseModel):
    food_category: str
    required_quantity_kg: float
    priority: str  # LOW, MEDIUM, HIGH, CRITICAL
    valid_until: datetime


class UpdateCapacityRequest(BaseModel):
    available_capacity_kg: float
