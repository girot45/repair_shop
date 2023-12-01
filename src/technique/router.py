import traceback

from fastapi import Depends, APIRouter, HTTPException

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_async_session
from src.technique.models import technique, client_tech
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
        print(receipt_number)
        query = (
            select(technique, client_tech.c.status,
                   client_tech.c.comments)
            .join(client_tech, client_tech.c.id_tech ==
                  technique.c.id)
            .filter(technique.c.id == receipt_number)
        )
        result = await session.execute(query)
        data = result.fetchone()
        print(data)
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
    except Exception as e:
        print()
        print()
        print()
        print(e)
        print()
        print()
        print()
        print("An error occurred:", e)
        traceback.print_exc()
        raise HTTPException(status_code=500, detail={
            "status": "error",
            "data": None
        })

