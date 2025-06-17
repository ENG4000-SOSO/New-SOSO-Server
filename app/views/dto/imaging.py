from datetime import datetime
from typing import Optional

from pydantic import BaseModel

class Recurrence(BaseModel):
    revisit: str
    number_of_revisits: Optional[int] = None
    revisit_frequency: Optional[int] = None
    revisit_frequency_units: Optional[str] = None

class CreateImageRequest(BaseModel):
    image_name: str
    mission_id: int
    latitude: float
    longitude: float
    priority: int
    image_type: Optional[str] = None
    image_start_time: datetime
    image_end_time: datetime
    delivery_time: datetime
    recurrence: Optional[Recurrence] = None
