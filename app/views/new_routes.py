# type: ignore

from datetime import datetime
import logging
from typing import Optional
from fastapi import APIRouter
from pydantic import BaseModel

logger = logging.getLogger(__name__)
router = APIRouter()

class GroundStationCreationRequest(BaseModel):
    name: str
    latitude: float
    longitude: float
    elevation: float
    send_mask: float
    receive_mask: float
    uplink_rate_mbps: float
    downlink_rate_mbps: float

# =============== DONE ===============
@router.post("/assets/groundstations/create")
async def new_ground_station(ground_station: GroundStationCreationRequest):
    # Creates a new ground station record and returns its ID.
    pass
# =============== ==== ===============

# =============== DONE ===============
class Recurrence(BaseModel):
    Revisit: str
    NumberOfRevisits: Optional[int] = None
    RevisitFrequency: Optional[int] = None
    RevisitFrequencyUnits: Optional[str] = None
# =============== ==== ===============

# =============== DONE ===============
class ImageRequest(BaseModel):
    Latitude: float
    Longitude: float
    Priority: int
    ImageType: str
    ImageStartTime: str
    ImageEndTime: str
    DeliveryTime: str
    Recurrence: Recurrence
# =============== ==== ===============

# =============== DONE ===============
@router.post("/imaging/orders/create")
async def create_order(image_request: ImageRequest):
    # Creates a new image order based on provided data.
    pass
# =============== ==== ===============

# =============== DONE ===============
@router.get("/assets/names")
async def get_names(asset_type: str = None):
    # Retrieves names of satellites and/or ground stations based on asset type.
    pass
# =============== ==== ===============

# =============== DONE ===============
class Window(BaseModel):
    Start: str
    End: str
# =============== ==== ===============

# =============== DONE ===============
class Frequency(BaseModel):
    MinimumGap: str
    MaximumGap: str
# =============== ==== ===============

# =============== DONE ===============
class RepeatCycle(BaseModel):
    Frequency: Frequency
    Repetition: str
# =============== ==== ===============

# =============== DONE ===============
class ActivityRequest(BaseModel):
    Target: str
    Activity: str
    Window: Window
    Duration: str
    RepeatCycle: RepeatCycle
    PayloadOutage: str
# =============== ==== ===============

# =============== DONE ===============
@router.post("/maintenance/orders/create")
async def create_maintenance_request(maintenance_request: ActivityRequest):
    # Creates a maintenance request for a specified satellite.
    pass
# =============== ==== ===============

# =============== DONE ===============
class OutageOrderCreationRequest(BaseModel):
    Target: str
    Activity: str
    Window: Window
# =============== ==== ===============

# =============== DONE ===============
@router.post("/outage/orders/create")
async def create_outage(outage_request: OutageOrderCreationRequest):
    # Creates an outage order for a specified asset.
    pass
# =============== ==== ===============

# =============== DONE ===============
@router.get("/maintenance/orders")
async def get_all_maintenance_orders(page: int = 1, per_page: int = 20, all: bool = False):
    # Retrieves all maintenance orders with pagination support.
    pass
# =============== ==== ===============

# =============== DONE ===============
@router.get("/imaging/orders")
async def get_all_image_orders(page: int = 1, per_page: int = 20, all: bool = False):
    # Retrieves all image orders with pagination support.
    pass
# =============== ==== ===============

# =============== DONE ===============
@router.get("/outage/orders")
async def get_all_outage_orders(asset_type: str = None, page: int = 1, per_page: int = 20, all: bool = False):
    # Retrieves all outage orders with optional filtering by asset type.
    pass
# =============== ==== ===============

@router.post("/maintenance/orders/{id}/requests/decline")
async def decline_maintenance_order_requests(id: int):
    # Declines all schedule requests related to a maintenance order.
    pass

@router.post("/imaging/orders/{id}/requests/decline")
async def decline_image_order_requests(id: int):
    # Declines all schedule requests related to an image order.
    pass

@router.post("/outage/orders/{id}/requests/decline")
async def decline_outage_order_requests(id: int):
    # Declines all schedule requests related to an outage order.
    pass

@router.get("/schedules/requests")
async def get_all_schedule_requests(order_ids: list = None, page: int = 1, per_page: int = 20, all: bool = False, order_types: list = None):
    # Retrieves schedule requests with optional filtering and pagination support.
    pass

@router.post("/schedules/requests/{request_id}/decline")
async def decline_schedule_request(request_id: int):
    # Declines a specific schedule request by ID.
    pass

@router.get("/schedules/{id}/events")
async def scheduled_events_by_id(id: int, page: int = 1, per_page: int = 1000, all: bool = False, event_types: list = None):
    # Retrieves scheduled events by schedule ID.
    pass

@router.get("/schedules/")
async def get_schedules(name: str = None):
    # Retrieves schedules by name or all schedules if no name is provided.
    pass

@router.get("/schedules/default")
async def get_default_schedule():
    # Retrieves the default schedule from the database.
    pass

@router.post("/schedules/{id}/set_reference_time")
async def set_schedule_reference_time(id: int, reference_time: datetime):
    # Sets a reference time for a given schedule.
    pass
