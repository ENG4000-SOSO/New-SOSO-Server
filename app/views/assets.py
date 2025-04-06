from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from app.models.assets import Satellite, GroundStation
from app.db.connection import get_db
from typing import Annotated
from starlette import status
from .auth import operator_required, get_current_user
from sqlalchemy.orm import Session
import logging

# Set up logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

router = APIRouter(
    prefix='/assets',
    tags=['assets']
)

db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]
operator_dependency = Annotated[bool, Depends(operator_required)]

# Request model for creating a satellite
class CreateSatelliteRequest(BaseModel):
    satellite_name: str
    storage_capacity: float
    power_capacity: float
    fov_max: float
    fov_min: float
    is_illuminated: bool
    under_outage: bool

# Request model for creating a ground station
class CreateGroundStationRequest(BaseModel):
    ground_station_name: str
    latitude: float
    longitude: float
    elevation: float
    station_mask: float
    uplink_rate: float
    downlink_rate: float
    under_outage: bool

# Satellite Endpoints

@router.post("/satellite", status_code=status.HTTP_201_CREATED)
async def create_satellite(db: db_dependency, user: user_dependency, operator: operator_dependency, create_satellite_request: CreateSatelliteRequest):
    """
    Create a new satellite asset.
    Accessible to authenticated operators.
    """
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication Failed')
    
    new_satellite = Satellite(
        satellite_name=create_satellite_request.satellite_name,
        storage_capacity=create_satellite_request.storage_capacity,
        power_capacity=create_satellite_request.power_capacity,
        fov_max=create_satellite_request.fov_max,
        fov_min=create_satellite_request.fov_min,
        is_illuminated=create_satellite_request.is_illuminated,
        under_outage=create_satellite_request.under_outage
    )
    db.add(new_satellite)
    db.commit()
    logger.info("Created satellite: %s", new_satellite.satellite_name)
    return {"message": "Satellite created successfully"}

@router.get("/satellites", status_code=status.HTTP_200_OK)
def fetch_all_satellites(db: db_dependency, user: user_dependency, operator: operator_dependency):
    """
    Fetch all satellites.
    """
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication Failed')
    satellites = db.query(Satellite).all()
    logger.info("Fetched all satellites")
    return {"satellites": satellites}

@router.get("/satellite/{satellite_id}", status_code=status.HTTP_200_OK)
def get_satellite(db: db_dependency, user: user_dependency, operator: operator_dependency, satellite_id: int):
    """
    Fetch a single satellite by its id.
    """
    if user is None:
        raise HTTPException(status_code=401, detail="Authentication Failed")
    satellite = db.query(Satellite).filter(Satellite.id == satellite_id).first()
    if satellite is not None:
        logger.info("Fetched satellite: %s", satellite.satellite_name)
        return satellite
    logger.warning("Satellite with id %s not found", satellite_id)
    raise HTTPException(status_code=404, detail='Item not found')

# Ground Station Endpoints

@router.post("/ground_station", status_code=status.HTTP_201_CREATED)
async def create_ground_station(db: db_dependency, user: user_dependency, operator: operator_dependency, create_ground_station_request: CreateGroundStationRequest):
    """
    Create a new ground station asset.
    """
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication Failed')
    
    new_station = GroundStation(
        ground_station_name=create_ground_station_request.ground_station_name,
        latitude=create_ground_station_request.latitude,
        longitude=create_ground_station_request.longitude,
        elevation=create_ground_station_request.elevation,
        station_mask=create_ground_station_request.station_mask,
        uplink_rate=create_ground_station_request.uplink_rate,
        downlink_rate=create_ground_station_request.downlink_rate,
        under_outage=create_ground_station_request.under_outage
    )
    db.add(new_station)
    db.commit()
    logger.info("Created ground station: %s", new_station.ground_station_name)
    return {"message": "Ground station created successfully"}

@router.get("/ground_stations", status_code=status.HTTP_200_OK)
def fetch_all_ground_stations(db: db_dependency, user: user_dependency, operator: operator_dependency):
    """
    Fetch all ground stations.
    """
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication Failed')
    stations = db.query(GroundStation).all()
    logger.info("Fetched all ground stations")
    return {"ground_stations": stations}

@router.get("/ground_station/{ground_station_id}", status_code=status.HTTP_200_OK)
def get_ground_station(db: db_dependency, user: user_dependency, operator: operator_dependency, ground_station_id: int):
    """
    Fetch a single ground station by its id.
    """
    if user is None:
        raise HTTPException(status_code=401, detail="Authentication Failed")
    station = db.query(GroundStation).filter(GroundStation.id == ground_station_id).first()
    if station is not None:
        logger.info("Fetched ground station: %s", station.ground_station_name)
        return station
    logger.warning("Ground station with id %s not found", ground_station_id)
    raise HTTPException(status_code=404, detail='Item not found')