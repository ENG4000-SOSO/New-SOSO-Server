from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from app.models.assets import Satellite, GroundStation
from app.db.connection import SessionLocal, get_db
from typing import Annotated
from starlette import status
from passlib.context import CryptContext
from .auth import operator_required, get_current_user
from sqlalchemy.orm import Session

router = APIRouter(
    prefix='/assets',
    tags=['assets']
)

db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]
operator_dependency = Annotated[bool, Depends(operator_required)]

class CreateSatelliteRequest(BaseModel):
    satellite_name: str
    storage_capacity: float
    power_capacity: float
    fov_max: float
    fov_min: float
    is_illuminated: bool
    under_outage: bool

class CreateGroundStationRequest(BaseModel):
    ground_station_name: str
    latitude: float
    longitude: float
    elevation: float
    station_mask: float
    uplink_rate: float
    downlink_rate: float
    under_outage: bool


# Satellite API Endpoints

# Add a satellite
@router.post("/satellite", status_code=status.HTTP_201_CREATED)
async def create_satellite(db: db_dependency, user: user_dependency, operator: operator_dependency, create_satellite_request: CreateSatelliteRequest):
    if user is None:
        raise HTTPException(status_code=401,detail='Authentication Failed')
    
    create_satellite_model = Satellite(
        satellite_name = create_satellite_request.satellite_name,
        storage_capacity = create_satellite_request.storage_capacity,
        power_capacity = create_satellite_request.power_capacity,
        fov_max = create_satellite_request.fov_max,
        fov_min = create_satellite_request.fov_min,
        is_illuminated = create_satellite_request.is_illuminated,
        under_outage = create_satellite_request.under_outage
    )
    db.add(create_satellite_model)
    db.commit()

# Get all satellites
@router.get("/satellites", status_code=status.HTTP_200_OK)
def fetch_all_satellites(db: db_dependency, user: user_dependency, operator: operator_dependency):
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication Failed')
    satellites = db.query(Satellite).all()
    return {"satellites": satellites}


# Get a single satelllite by ID
@router.get("/satellite/{satellite_id}", status_code=status.HTTP_200_OK)
def get_satellite(db: db_dependency, user: user_dependency, operator: operator_dependency, satellite_id: int):
    if user is None:
        raise HTTPException(status_code=401, detail="Authentication Failed")
    satellite_model = db.query(Satellite).filter(Satellite.id == satellite_id).first()
    if satellite_model is not None:
        return satellite_model
    raise HTTPException(status_code=404, detail='Item not found')

# Ground Station API Endpoints
# Add a satellite
@router.post("/ground_station", status_code=status.HTTP_201_CREATED)
async def create_ground_station(db: db_dependency, user: user_dependency, operator: operator_dependency, create_ground_station_request: CreateGroundStationRequest):
    if user is None:
        raise HTTPException(status_code=401,detail='Authentication Failed')
    
    create_ground_station_model = GroundStation(
        ground_station_name = create_ground_station_request.ground_station_name,
        latitude = create_ground_station_request.latitude,
        longitude = create_ground_station_request.longitude,
        elevation = create_ground_station_request.elevation,
        station_mask = create_ground_station_request.station_mask,
        uplink_rate = create_ground_station_request.uplink_rate,
        downlink_rate = create_ground_station_request.downlink_rate,
        under_outage = create_ground_station_request.under_outage
    )
    db.add(create_ground_station_model)
    db.commit()

# Get all ground stations
@router.get("/ground_stations", status_code=status.HTTP_200_OK)
def fetch_all_ground_stations(db: db_dependency, user: user_dependency, operator: operator_dependency):
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication Failed')
    ground_stations = db.query(GroundStation).all()
    return {"GroundStation": ground_stations}

# Get a single ground station by ID
@router.get("/ground_station/{ground_station_id}", status_code=status.HTTP_200_OK)
def get_satellite(db: db_dependency, user: user_dependency, operator: operator_dependency, ground_station_id: int):
    if user is None:
        raise HTTPException(status_code=401, detail="Authentication Failed")
    ground_station_model = db.query(GroundStation).filter(GroundStation.id == ground_station_id).first()
    if ground_station_model is not None:
        return ground_station_model
    raise HTTPException(status_code=404, detail='Item not found')
