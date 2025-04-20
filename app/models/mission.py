from app.db.base import Base
from sqlalchemy import Column, Integer, String
from sqlalchemy.types import TIMESTAMP

class Mission(Base):
    __tablename__ = "mission"

    id = Column(Integer, primary_key=True, index=True)
    mission_name = Column(String, nullable=False)
    mission_start = Column(TIMESTAMP, nullable=False)
    mission_end = Column(TIMESTAMP, nullable=False)
