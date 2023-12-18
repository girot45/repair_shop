from fastapi import Depends, APIRouter

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.auth_config import current_user
from src.auth.models import User
from src.crm.models import ClientTech, Client
from src.crm.utils import prepare_data, prepare_clients_answer
from src.crm.schemas import CreateClientTech, ResponseClientTech, \
    CreateNewClient, ResponseClient
from src.database import get_async_session

router = APIRouter(
    prefix="/orders",
    tags=["Orders"]
)


@router.get("/get_all_orders", response_model=ResponseClientTech)
async def get_all_orders(
        user: User = Depends(current_user),
        session: AsyncSession = Depends(get_async_session)
):
    try:
        if not user.is_admin:
            return {"status": "error", "data": "You are not an admin"}
        query = select(ClientTech).order_by(ClientTech.acceptance_date)

        res = await session.execute(query)
        pre_data = res.scalars()
        answer = prepare_data(pre_data)
        return {"status": "success", "data": answer}
    except Exception as e:
        return {"status": "error", "data": str(e)}


@router.get("/get_orders_without_master", response_model=ResponseClientTech)
async def get_orders_without_master(
        user: User = Depends(current_user),
        session: AsyncSession = Depends(get_async_session)
):
    try:
        stmt = (
            select(ClientTech)
            .filter(ClientTech.id_master.is_(None))
        )
        res = await session.execute(stmt)
        pre_data = res.scalars()
        answer = prepare_data(pre_data)
        return {"status": "success", "data": answer}
    except Exception as e:
        return {"status": "error", "data": str(e)}


@router.get("/get_master_orders", response_model=ResponseClientTech)
async def get_master_orders(
        user: User = Depends(current_user),
        session: AsyncSession = Depends(get_async_session)
):
    try:
        if user.is_admin:
            return {"status": "error", "data": "You are not a master"}
        stmt = (
            select(ClientTech)
            .filter(ClientTech.id_master == user.id)
            .order_by(ClientTech.acceptance_date)
        )
        res = await session.execute(stmt)
        pre_data = res.scalars()
        answer = prepare_data(pre_data)
        return {"status": "success", "data": answer}
    except Exception as e:
        return {"status": "error", "data": str(e)}


@router.post("/create_order", response_model=ResponseClientTech)
async def create_order(

        data: CreateClientTech,
        user: User = Depends(current_user),
        session: AsyncSession = Depends(get_async_session)
):
    try:

        if not user.is_admin:
            return {"status": "error", "data": "You are not a admin"}
        stmt = (select(ClientTech).filter(
            ClientTech.id_tech == data.id_tech))
        res = await session.execute(stmt)
        pre_data = res.scalar()
        if pre_data:
            return {"status": "error", "data": "Order is already taken"}
        new_order = ClientTech(
            status=data.status,
            comments=data.comments,
            passport=data.passport,
            id_master=None,
            id_tech=data.id_tech
        )
        session.add(new_order)
        await session.commit()
        return {"status": "success", "data": "New order created"}
    except Exception as e:
        await session.rollback()
        return {"status": "error", "data": str(e)}


@router.put("/master_to_order", response_model=ResponseClientTech)
async def master_to_order(
        id_tech: int,
        user: User = Depends(current_user),
        session: AsyncSession = Depends(get_async_session)
):
    try:
        if user.is_admin:
            return {"status": "error", "data": "You are not a master"}
        stmt = (
            select(ClientTech)
            .filter(ClientTech.id_tech == id_tech)
            .filter(ClientTech.id_master.is_(None))
        )
        res = await session.execute(stmt)
        data = res.scalar()
        if not data:
            return {"status": "error", "data": "This order is not available"}
        stmt = (
            update(ClientTech)
            .where(ClientTech.id_tech == id_tech)
            .values(id_master=user.id)
        )
        await session.execute(stmt)
        await session.commit()
        return {"status": "success", "data": "You got an order"}
    except Exception as e:
        await session.rollback()
        return {"status": "error", "data": str(e)}

@router.post("/create_client", response_model=ResponseClient)
async def create_client(
        client: CreateNewClient,
        user: User = Depends(current_user),
        session: AsyncSession = Depends(get_async_session)
):
    try:
        if not user.is_admin:
            return {"status": "error", "data": "You are not an admin"}
        stmt = (select(Client).filter(Client.passport == client.passport))
        res = await session.execute(stmt)
        client_answer = res.scalar()
        if client_answer:
            return {"status": "error", "data": "This client already exists"}
        else:
            new_client = Client(
                passport=client.passport,
                fio=client.fio,
                phone=client.phone,
                email=client.email,
            )
            session.add(new_client)
            await session.commit()
            return {"status": "success", "data": "New client created"}
    except Exception as e:
        await session.rollback()
        return {"status": "error", "data": str(e)}


@router.get("/get_all_clients", response_model=ResponseClient)
async def get_all_clients(
        user: User = Depends(current_user),
        session: AsyncSession = Depends(get_async_session)
):
    try:
        if not user.is_admin:
            return {"status": "error", "data": "You are not an admin"}
        stmt = (
            select(Client))
        res = await session.execute(stmt)
        clients = res.scalars()
        answer = prepare_clients_answer(clients)
        return {"status": "success", "data": answer}
    except Exception as e:
        return {"status": "error", "data": str(e)}