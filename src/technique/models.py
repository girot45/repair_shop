from sqlalchemy import Table, Column, Integer, text, \
    String, ForeignKey, DATE, JSON, BigInteger, Sequence

from src.auth.models import master
from src.database import metadata


client = Table(
    "Client",
    metadata,
    Column("passport", String, primary_key=True),
    Column("fio", String, nullable=False),
    Column("phone", String, unique=True, nullable=False),
    Column("email", String, unique=True, nullable=False)
)

technique = Table(
    "Technique",
    metadata,
    Column("id", BigInteger, Sequence('tech_id_seq'),
           primary_key=True,
           server_default=text('nextval(\'tech_id_seq\'::regclass)')),
    Column("name", String, nullable=False),
    Column("model", String, nullable=False),
    Column("acceptance_date", DATE, nullable=False),
    Column("breakdown_description", String, nullable=False),
    Column("damaged_details", JSON, nullable=False)
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
    )
)
