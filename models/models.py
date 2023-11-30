from sqlalchemy import MetaData, Table, Column, Integer, \
    String, ForeignKey, DATE, JSON, Boolean, BigInteger, Sequence

metadata = MetaData()


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
           server_default="1"),
    Column("name", String, nullable=False),
    Column("model", String, nullable=False),
    Column("acceptance_date", DATE, nullable=False),
    Column("breakdown_description", String, nullable=False),
    Column("damaged_details", JSON, nullable=False)
)

master = Table(
    "Master",
    metadata,
    Column("id", BigInteger, Sequence('master_id_seq'),
           primary_key=True,
           server_default="1"),
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
    Column("comments", String, nullable=False),
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
