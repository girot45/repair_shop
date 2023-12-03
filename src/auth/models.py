from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTable
from sqlalchemy import (
    Table, Column, Integer, String,
    DATE, Boolean, BigInteger, Sequence, text
)

from src.database import Base, metadata


master = Table(
    "Master",
    metadata,
    Column("id", BigInteger, Sequence('master_id_seq'),
           primary_key=True,
           server_default=text('nextval(\'master_id_seq\'::regclass)')),
    Column("hashed_password", String, nullable=False),
    Column("email", String, nullable=False),
    Column("fio", String, nullable=False),
    Column("age", Integer, nullable=False),
    Column("date_of_hire", DATE, nullable=False),
    Column("exp", Integer, nullable=False),
    Column("speciality", String, nullable=False),
    Column("is_admin", Integer, server_default="0",
           nullable=False),
    Column("is_active", Boolean, default=True, nullable=False),
    Column("is_superuser", Boolean, default=False, nullable=False),
    Column("is_verified", Boolean, default=False, nullable=False),
)


class User(SQLAlchemyBaseUserTable[int], Base):
    __tablename__ = "Master"
    id = Column(BigInteger, primary_key=True)
    email = Column(String, nullable=False)
    hashed_password = Column(String, nullable=False)
    fio = Column(String, nullable=False)
    age = Column(Integer, nullable=False)
    date_of_hire = Column(DATE, nullable=False)
    exp = Column(Integer, nullable=False)
    speciality = Column(String, nullable=False)
    is_admin: int = Column(Integer, server_default="0",nullable=False)
    is_active: bool = Column(Boolean, default=True, nullable=False)
    is_superuser: bool = Column(Boolean, default=False,
                                nullable=False)
    is_verified: bool = Column(Boolean, default=False, nullable=False)
