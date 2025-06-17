from app.db.base import Base
from sqlalchemy import Column, Integer, String, Boolean, Double
from sqlalchemy.types import TIMESTAMP

class ActivityRequest(Base):
    __tablename__ = "activity_request"

    id = Column(Integer, primary_key=True, index=True)
    target = Column(String, nullable=False)
    activity = Column(String, nullable=False)
    window_start = Column(TIMESTAMP, nullable=False)
    window_end = Column(TIMESTAMP, nullable=False)
    duration = Column(String, nullable=False)
    repeat_cycle_repetition = Column(String, nullable=True)
    repeat_cycle_frequency_minimum_gap = Column(String, nullable=True)
    repeat_cycle_frequency_maximum_gap = Column(String, nullable=True)
    payload_outage = Column(String, nullable=False)
