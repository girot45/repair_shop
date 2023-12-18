import json

from fastapi import Depends, APIRouter

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.auth_config import current_user
from src.auth.models import User
from src.crm.models import ClientTech
from src.database import get_async_session
from src.technique.models import Technique
from src.technique.schemas import TechReturn, TechCreate, \
    ResponseTech

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
            select(Technique, ClientTech.status,
                   ClientTech.comments, ClientTech.acceptance_date)
            .join(ClientTech, ClientTech.id_tech == Technique.id)
            .filter(Technique.id == receipt_number)
        )
        result = await session.execute(query)
        pre_data = result.fetchone()
        print(pre_data)
        if pre_data:
            tech, status, comments, acceptance_date = pre_data
            res_dict = {
                "id": tech.id,
                "name": tech.name,
                "model": tech.model,
                "acceptance_date": acceptance_date,
                "breakdown_description": tech.breakdown_description,
                "damaged_details": tech.damaged_details["details"],
                "repair_status": status,
                "comments": comments
            }
        else:
            res_dict = None
        return {"status": "success", "data": res_dict}
    except Exception as e:
        return {"status": "error", "data": str(e)}


@router.post("/create_technique", response_model=ResponseTech)
async def create_technique(
        technique: TechCreate,
        user: User = Depends(current_user),
        session: AsyncSession = Depends(get_async_session)
):
    try:
        damaged_details_json = [item.__dict__ for item in technique.damaged_details]
        damaged_details = {"details": damaged_details_json}
        new_tech = Technique(
            name=technique.name,
            model=technique.model,
            breakdown_description=technique.breakdown_description,
            damaged_details=damaged_details
        )
        session.add(new_tech)
        await session.commit()
        return {"status": "success", "message": "New tech added"}
    except Exception as e:
        await session.rollback()
        return {"status": "error", "message": str(e)}


@router.delete("/delete_technique", response_model=ResponseTech)
async def delete_technique(
        id_tech: int,
        session: AsyncSession = Depends(get_async_session),
        user: User = Depends(current_user)
):
    try:
        if not user.is_admin:
            return {"status": "error", "data": "You are not an admin"}
        stmt = (select(Technique).filter(Technique.id == id_tech))
        res = await session.execute(stmt)
        data = res.scalar()
        if not data:
            return {"status": "error", "data": "No such technique"}

        else:
            stmt = select(ClientTech).filter(ClientTech.id_tech ==id_tech)
            res = await session.execute(stmt)
            client_tech_record = res.scalar()
            if client_tech_record:
                await session.delete(client_tech_record)
            await session.delete(data)
            await session.commit()
            return {
                "status": "success", "message": "Technique deleted"
            }
    except Exception as e:
        await session.rollback()
        return {"status": "error", "data": str(e)}