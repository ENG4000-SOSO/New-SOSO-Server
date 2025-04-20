from app.db.base import Base
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Double
from sqlalchemy.types import Enum

class Satellite(Base):
    __tablename__ = "satellite"

    id = Column(Integer, primary_key=True, index=True)
    satellite_name = Column(String, nullable=False)
    tle_line1 = Column(String, nullable=False)
    tle_line2 = Column(String, nullable=False)
    storage_capacity = Column(Double)
    power_capacity = Column(Double)
    fov_max = Column(Double)
    fov_min = Column(Double)
    is_illuminated = Column(Boolean, default=False)
    under_outage = Column(Boolean, default=False)

class GroundStation(Base):
    __tablename__ = "ground_station"

    id = Column(Integer, primary_key=True, index=True)
    ground_station_name = Column(String, nullable=False)
    latitude = Column(Double, nullable=False)
    longitude = Column(Double, nullable=False)
    elevation = Column(Double, nullable=False)
    send_mask = Column(Double)
    receive_mask = Column(Double)
    uplink_rate = Column(Double, nullable=False)
    downlink_rate = Column(Double, nullable=False)
    under_outage = Column(Boolean, default=False)
