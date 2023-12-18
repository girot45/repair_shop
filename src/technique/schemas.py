from datetime import date, datetime
from typing import Optional, Any
from pydantic import BaseModel


class DamagedDetails(BaseModel):
    descr: str


class TechRead(BaseModel):
    id: int
    name: str
    model: str
    acceptance_date: datetime
    breakdown_description: str
    damaged_details: list[DamagedDetails]
    repair_status: str
    comments: str


class TechReturn(BaseModel):
    status: str
    data: Optional[TechRead]

class TechCreate(BaseModel):
    name: str
    model: str
    breakdown_description: str
    damaged_details: list[DamagedDetails]


class ResponseTech(BaseModel):
    status: str
    message: str