"""
This module defines the models for satellite assets and ground stations.
Each model inherits from the SQLAlchemy Base, which is configured in db/base.py.
"""

from app.db.base import Base
from sqlalchemy import Column, Integer, String, Boolean, Double
from sqlalchemy.types import Enum

class Satellite(Base):
    """
    Satellite model represents a satellite asset with key operational parameters.
    """
    __tablename__ = "satellite"

    id = Column(Integer, primary_key=True, index=True)
    satellite_name = Column(String, nullable=False, unique=True)  # Unique satellite name
    storage_capacity = Column(Double, nullable=False)  # Storage capacity (e.g., in GB)
    power_capacity = Column(Double, nullable=False)      # Power capacity (e.g., in Watts)
    fov_max = Column(Double, nullable=False)             # Maximum field-of-view (FOV)
    fov_min = Column(Double, nullable=False)             # Minimum field-of-view (FOV)
    is_illuminated = Column(Boolean, default=False)        # Indicates if the satellite is illuminated
    under_outage = Column(Boolean, default=False)          # Indicates if the satellite is under outage

    def __repr__(self):
        return f"<Satellite(id={self.id}, name='{self.satellite_name}')>"


class GroundStation(Base):
    """
    GroundStation model represents a ground station asset with key location and operational parameters.
    """
    __tablename__ = "ground_station"

    id = Column(Integer, primary_key=True, index=True)
    ground_station_name = Column(String, nullable=False, unique=True)  # Unique ground station name
    latitude = Column(Double, nullable=False)
    longitude = Column(Double, nullable=False)
    elevation = Column(Double, nullable=False)
    station_mask = Column(Double, nullable=False)   # Masking angle or similar parameter
    uplink_rate = Column(Double, nullable=False)      # Uplink data rate (e.g., in Mbps)
    downlink_rate = Column(Double, nullable=False)    # Downlink data rate (e.g., in Mbps)
    under_outage = Column(Boolean, default=False)      # Indicates if the ground station is under outage

    def __repr__(self):
        return f"<GroundStation(id={self.id}, name='{self.ground_station_name}')>"