from datetime import date, datetime
from typing import Optional, Any
from pydantic import BaseModel


class ReadAllOrders(BaseModel):
    status: str
    acceptance_date: datetime
    master_fio: str
    client_phone: str
