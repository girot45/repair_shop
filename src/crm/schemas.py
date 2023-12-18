from datetime import date, datetime
from typing import Optional, Any, List
from pydantic import BaseModel


class CreateClientTech(BaseModel):
    passport: str
    status: str
    comments: str
    id_tech: int


class ClientTechItems(BaseModel):
    id_tech: int
    passport: str
    status: str
    comments: str
    details_fo_client: Optional[int]
    id_master: Optional[int]
    acceptance_date: datetime


class ResponseClientTech(BaseModel):
    status: str
    data: Optional[List[ClientTechItems] | str]