from pprint import pprint

from faker import Faker
from datetime import datetime, timedelta
import random

from fastapi import APIRouter, Depends
from passlib.context import CryptContext
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.manager import UserManager, get_user_manager
from src.auth.models import Master
from src.crm.models import Client, ClientTech
from src.database import get_async_session
from src.technique.models import Technique

fake = Faker()

def generate_fake_master():
    fake_master = {
        "email": fake.email(),
        "password": fake.password(),
        "is_active": True,
        "is_superuser": False,
        "is_verified": False,
        "fio": fake.name(),
        "age": fake.random_int(min=18, max=65),
        "date_of_hire": (datetime.now() - timedelta(days=random.randint(365, 365*5))),
        "exp": fake.random_int(min=0, max=20),
        "speciality": fake.job(),
        "is_admin": 0
    }
    return fake_master

def generate_fake_tech():
    fake_tech = {
        "name": fake.word(),
        "model": fake.word(),
        "breakdown_description": fake.text(max_nb_chars=50),
        "damaged_details": {"details": [{"descr": "fake"}]}
    }
    return fake_tech

def generate_fake_client():
    fake_client = {
        "passport": fake.word(),
        "fio": fake.word(),
        "phone": fake.word(),
        "email": fake.word()
    }
    return fake_client


# Пример использования
fake_masters = [generate_fake_master() for _ in range(10)]

fake_techs = [generate_fake_tech() for _ in range(10)]
fake_clients = [generate_fake_client() for _ in range(10)]

def generate_fake_client_techs():
    res = []
    for i in range(10):
        fake_client_tech = {
            "id_tech": i+1,
            "passport": fake_clients[i]["passport"],
            "status": fake.word(),
            "comments": fake.text(max_nb_chars=50),
            "details_fo_client": random.randint(0, 6),
            "id_master": i+1 if random.randint(0, 10) % 2 else None,
            "acceptance_date": (datetime.now() - timedelta(days=random.randint(365, 365*5))).strftime("%Y-%m-%d"),
        }
        res.append(fake_client_tech)
    return res

fake_clients_techs = generate_fake_client_techs()


router = APIRouter(
    prefix="/insert_fake_data",
    tags=["Insert_fake_data"]
)



@router.post("")
async def insert_fake_client(
        session: AsyncSession = Depends(get_async_session)
):
    try:
        password_context = CryptContext(schemes=["bcrypt"],
                                        deprecated="auto")
        for fake_master in fake_masters:
            hashed_password = password_context.hash(fake_master["password"])
            new_master = Master(
                email=fake_master["email"],
                hashed_password=hashed_password,
                fio=fake_master["fio"],
                age=fake_master["age"],
                date_of_hire=fake_master["date_of_hire"],
                exp=fake_master["exp"],
                speciality=fake_master["speciality"],
                is_admin=fake_master["is_admin"],
                is_active=fake_master["is_active"],
                is_superuser=fake_master["is_superuser"],
                is_verified=fake_master["is_verified"],
            )
            session.add(new_master)
            await session.commit()
        for fake_tech in fake_techs:
            new_tech = Technique(
                name=fake_tech["name"],
                model=fake_tech["model"],
                breakdown_description=fake_tech["breakdown_description"],
                damaged_details=fake_tech["damaged_details"]
            )
            session.add(new_tech)
            await session.commit()
        for fake_client in fake_clients:
            new_client = Client(
                passport=fake_client["passport"],
                fio=fake_client["fio"],
                phone=fake_client["phone"],
                email=fake_client["email"],
            )
            session.add(new_client)
            await session.commit()
        for fake_clients_tech in fake_clients_techs:
            new_order = ClientTech(
                status=fake_clients_tech["status"],
                comments=fake_clients_tech["comments"],
                passport=fake_clients_tech["passport"],
                id_master=fake_clients_tech["id_master"],
                id_tech=fake_clients_tech["id_tech"],
                details_fo_client=fake_clients_tech["details_fo_client"]
            )
            session.add(new_order)
            await session.commit()
        return {"message": "success"}
    except Exception as e:
        return {"message":str(e)}