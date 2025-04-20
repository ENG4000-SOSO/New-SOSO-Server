from typing import Optional

from pydantic import BaseModel

class CreateSatelliteRequest(BaseModel):
    satellite_name: str
    tle_line1: str
    tle_line2: str
    storage_capacity: Optional[float] = None
    power_capacity: Optional[float] = None
    fov_max: Optional[float] = None
    fov_min: Optional[float] = None
    is_illuminated: Optional[bool] = None
    under_outage: Optional[bool] = None

class CreateGroundStationRequest(BaseModel):
    ground_station_name: str
    latitude: float
    longitude: float
    elevation: float
    send_mask: Optional[float] = None
    receive_mask: Optional[float] = None
    uplink_rate: float
    downlink_rate: float
    under_outage: Optional[bool] = None
