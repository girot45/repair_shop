from sqlalchemy import Table, Column, Integer, \
    String, ForeignKey, DateTime, BigInteger, func

from src.auth.models import master
from src.database import metadata
from src.technique.models import technique


client = Table(
    "Client",
    metadata,
    Column("passport", String, primary_key=True),
    Column("fio", String, nullable=False),
    Column("phone", String, unique=True, nullable=False),
    Column("email", String, unique=True, nullable=False)
)

client_tech = Table(
    "Client_tech",
    metadata,
    Column("id_tech", BigInteger, ForeignKey(
        technique.c.id,
        onupdate="cascade",
    ),
           primary_key=True
           ),
    Column(
        "passport",
        String,
        ForeignKey(
            client.c.passport,
            onupdate="cascade",
            ondelete="cascade"
        )
    ),
    Column("status", String, nullable=False),
    Column("comments", String, nullable=True),
    Column("details_fo_client", Integer, server_default="0",
           nullable=False),
    Column(
        "id_master",
        BigInteger,
        ForeignKey(
            master.c.id,
            onupdate="cascade",
            ondelete="set null"
        )
    ),
    Column("acceptance_date", DateTime(timezone=True),
           nullable=False,
           server_default=func.now()),
)