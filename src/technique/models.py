from sqlalchemy import Table, Column, text, \
    String, DATE, JSON, BigInteger, Sequence

from src.database import metadata, Base


class Technique(Base):
    __tablename__ = "Technique"
    metadata = metadata

    id = Column(BigInteger, Sequence('tech_id_seq'), primary_key=True,
                server_default=text('nextval(\'tech_id_seq\'::regclass)'))
    name = Column(String, nullable=False)
    model = Column(String, nullable=False)
    breakdown_description = Column(String, nullable=False)
    damaged_details = Column(JSON, nullable=False)
