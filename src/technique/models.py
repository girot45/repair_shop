from sqlalchemy import Table, Column, text, \
    String, DATE, JSON, BigInteger, Sequence

from src.database import metadata


technique = Table(
    "Technique",
    metadata,
    Column("id", BigInteger, Sequence('tech_id_seq'),
           primary_key=True,
           server_default=text('nextval(\'tech_id_seq\'::regclass)')),
    Column("name", String, nullable=False),
    Column("model", String, nullable=False),
    Column("breakdown_description", String, nullable=False),
    Column("damaged_details", JSON, nullable=False)
)
