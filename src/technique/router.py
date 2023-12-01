from fastapi import Depends, APIRouter, HTTPException

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_async_session
from src.technique.models import technique
from src.technique.schemas import TechReturn

router = APIRouter(
    prefix="/technique",
    tags=["Technique"]
)


@router.get("/info", response_model=TechReturn)
async def info(
        receipt_number: int,
        session: AsyncSession = Depends(get_async_session)
) -> TechReturn:
    try:
        query = (
            select(technique)
            .filter(technique.c.id == receipt_number)
        )
        result = await session.execute(query)
        data = result.fetchone()
        if data:
            res_dict = {
                "id": data.id,
                "name": data.name,
                "model": data.model,
                "acceptance_date": data.acceptance_date,
                "breakdown_description": data.breakdown_description,
                "damaged_details": data.damaged_details["details"]
            }
        else:
            res_dict = None
        user_answer: TechReturn = {"status": "success", "data": res_dict}
        return user_answer
    except:
        raise HTTPException(status_code=500, detail={
            "status": "error",
            "data": None
        })

