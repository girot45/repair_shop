from sqlalchemy import Column, Integer, \
    String, ForeignKey, DateTime, BigInteger, func

from src.auth.models import Master
from src.database import metadata, Base
from src.technique.models import Technique

class Client(Base):
    __tablename__ = "Client"

    metadata = metadata

    passport = Column(String, primary_key=True)
    fio = Column(String, nullable=False)
    phone = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)


class ClientTech(Base):
    __tablename__ = "Client_tech"
    metadata = metadata

    id_tech = Column(BigInteger, ForeignKey("Technique.id", onupdate="cascade"), primary_key=True)
    passport = Column(String, ForeignKey("Client.passport", onupdate="cascade", ondelete="cascade"))
    status = Column(String, nullable=False)
    comments = Column(String, nullable=True)
    details_fo_client = Column(Integer, server_default="0", nullable=False)
    id_master = Column(BigInteger,
                       ForeignKey("Master.id", onupdate="cascade", ondelete="set null"),
                       nullable=True)
    acceptance_date = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
