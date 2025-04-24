from app.db.base import Base
from sqlalchemy import Column, Integer, UUID, String, Boolean, ForeignKey, Double
from sqlalchemy.types import TIMESTAMP


class ScheduleRequest(Base):
    __tablename__ = "schedule_request"

    id = Column(UUID(as_uuid=True), primary_key=True, index=True)
    mission_id = Column(Integer, ForeignKey("mission.id"), nullable=False)
    created_at = Column(TIMESTAMP, nullable=True)
    updated_at = Column(TIMESTAMP, nullable=True)
    input_object_key = Column(String, nullable=True)
    output_object_key = Column(String, nullable=True)
    status = Column(String, nullable=True)
