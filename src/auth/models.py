from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTable
from sqlalchemy import (
    Table, Column, Integer, String,
    DATE, Boolean, BigInteger, Sequence, text
)

from src.database import Base, metadata


class Master(Base):
    __tablename__ = "Master"
    metadata = metadata
    id = Column(BigInteger, primary_key=True)
    email = Column(String, nullable=False)
    hashed_password = Column(String, nullable=False)
    fio = Column(String, nullable=False)
    age = Column(Integer, nullable=False)
    date_of_hire = Column(DATE, nullable=False)
    exp = Column(Integer, nullable=False)
    speciality = Column(String, nullable=False)
    is_admin: int = Column(Integer, server_default="0", nullable=False)
    is_active: bool = Column(Boolean, default=True, nullable=False)
    is_superuser: bool = Column(Boolean, default=False,
                                nullable=False)
    is_verified: bool = Column(Boolean, default=False, nullable=False)


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
    is_admin: int = Column(Integer, server_default="0",
                           nullable=False)
    is_active: bool = Column(Boolean, default=True, nullable=False)
    is_superuser: bool = Column(Boolean, default=False,
                                nullable=False)
    is_verified: bool = Column(Boolean, default=False, nullable=False)
