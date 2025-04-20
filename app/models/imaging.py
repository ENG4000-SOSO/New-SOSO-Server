from app.db.base import Base
from sqlalchemy import Column, Integer, String, Boolean, Double, ForeignKey
from sqlalchemy.types import TIMESTAMP

class ImageRequest(Base):
    __tablename__ = "image_request"

    id = Column(Integer, primary_key=True, index=True)
    mission_id = Column(Integer, ForeignKey("mission.id"), nullable=False)
    image_name = Column(String, nullable=False)
    latitude = Column(Double, nullable=False)
    longitude = Column(Double, nullable=False)
    priority = Column(Integer, nullable=False)
    image_type = Column(String)
    image_start_time = Column(TIMESTAMP, nullable=False)
    image_end_time = Column(TIMESTAMP, nullable=False)
    delivery_time = Column(TIMESTAMP, nullable=False)
    recurrence_revisit = Column(String)
    recurrence_number_of_revisits = Column(Integer)
    recurrence_revisit_frequency = Column(Integer)
    recurrence_revisit_frequency_units = Column(String)
