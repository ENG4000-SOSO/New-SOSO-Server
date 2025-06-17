from app.db.base import Base
from sqlalchemy import Column, Integer, String, Boolean, Double
from sqlalchemy.types import TIMESTAMP

class OutageRequest(Base):
    __tablename__ = "outage_request"

    id = Column(Integer, primary_key=True, index=True)
    target = Column(String, nullable=False)
    activity = Column(String, nullable=False)
    window_start = Column(TIMESTAMP, nullable=False)
    window_end = Column(TIMESTAMP, nullable=False)
