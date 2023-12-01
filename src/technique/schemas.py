from datetime import date
from typing import Optional, Any
from pydantic import BaseModel


class DamagedDetails(BaseModel):
    descr: str


class TechRead(BaseModel):
    id: int
    name: str
    model: str
    acceptance_date: date
    breakdown_description: str
    damaged_details: list[DamagedDetails]


class TechReturn(BaseModel):
    status: str
    data: Optional[TechRead | None]