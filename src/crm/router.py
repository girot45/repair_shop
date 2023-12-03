import traceback
from datetime import date, timedelta, datetime
from typing import Optional

from fastapi import Depends, APIRouter, HTTPException

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.auth_config import current_user
from src.auth.models import User
from src.crm.models import client_tech
from src.database import get_async_session
from src.technique.models import technique
from src.technique.schemas import TechReturn

router = APIRouter(
    prefix="/orders",
    tags=["Orders"]
)


@router.get("/all")
async def get_all_orders(
        user: User = Depends(current_user),
        acceptance_date: Optional[datetime, None] = datetime.now() -
                                                    timedelta(days=7),
        offset: Optional[int, None] = 5,
        status: Optional[int, None] = None,
        master: Optional[int, None] = None,
):
    try:
        if not user.is_admin:
            return "123"
        query = select(client_tech)
    except:
        pass


@router.get("")
async def get_orders_by_master_id(
        user: User = Depends(current_user),
        offset: Optional[int, None] = 5,
        status: Optional[int, None] = None,
):
    pass
