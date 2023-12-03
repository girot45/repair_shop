from fastapi import Depends, APIRouter, HTTPException

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.crm.models import client_tech
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
            select(technique, client_tech.c.status,
                   client_tech.c.comments, client_tech.c.acceptance_date)
            .join(client_tech, client_tech.c.id_tech ==
                  technique.c.id)
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
                "damaged_details": data.damaged_details["details"],
                "repair_status": data.status,
                "comments": data.comments
            }
        else:
            res_dict = None

        return {"status": "success", "data": res_dict}
    except:
        raise HTTPException(status_code=500, detail={
            "status": "error",
            "data": None
        })

