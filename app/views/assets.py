from fastapi import APIRouter, HTTPException, Query
from fastapi.encoders import jsonable_encoder
from starlette import status

from app.models.assets import Satellite, GroundStation
from app.utils.auth import db_dependency, user_dependency, operator_dependency
from app.views.dto.assets import CreateGroundStationRequest, CreateSatelliteRequest

router = APIRouter(
    prefix='/assets',
    tags=['assets']
)

# Satellite API Endpoints

# Add a satellite
@router.post("/satellite", status_code=status.HTTP_201_CREATED)
async def create_satellite(db: db_dependency, user: user_dependency, operator: operator_dependency, create_satellite_request: CreateSatelliteRequest):
    if user is None:
        raise HTTPException(status_code=401,detail='Authentication Failed')
    
    create_satellite_model = Satellite(
        satellite_name = create_satellite_request.satellite_name,
        tle_line1 = create_satellite_request.tle_line1,
        tle_line2 = create_satellite_request.tle_line2,
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
    return jsonable_encoder(satellites)


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
@router.post("/groundstations/create", status_code=status.HTTP_201_CREATED)
async def create_ground_station(db: db_dependency, user: user_dependency, operator: operator_dependency, create_ground_station_request: CreateGroundStationRequest):
    if user is None:
        raise HTTPException(status_code=401,detail='Authentication Failed')
    
    create_ground_station_model = GroundStation(
        ground_station_name = create_ground_station_request.ground_station_name,
        latitude = create_ground_station_request.latitude,
        longitude = create_ground_station_request.longitude,
        elevation = create_ground_station_request.elevation,
        send_mask = create_ground_station_request.send_mask,
        receive_mask = create_ground_station_request.receive_mask,
        uplink_rate = create_ground_station_request.uplink_rate,
        downlink_rate = create_ground_station_request.downlink_rate,
        under_outage = False
    )
    db.add(create_ground_station_model)
    db.commit()

# Get all ground stations
@router.get("/ground_stations", status_code=status.HTTP_200_OK)
def fetch_all_ground_stations(db: db_dependency, user: user_dependency, operator: operator_dependency):
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication Failed')
    ground_stations = db.query(GroundStation).all()
    return ground_stations

# Get a single ground station by ID
@router.get("/ground_station/{ground_station_id}", status_code=status.HTTP_200_OK)
def get_ground_station(db: db_dependency, user: user_dependency, operator: operator_dependency, ground_station_id: int):
    if user is None:
        raise HTTPException(status_code=401, detail="Authentication Failed")
    ground_station_model = db.query(GroundStation).filter(GroundStation.id == ground_station_id).first()
    if ground_station_model is not None:
        return ground_station_model
    raise HTTPException(status_code=404, detail='Item not found')

@router.get("/names")
async def get_names(db: db_dependency, user: user_dependency, asset_type: str = Query(None)):
    if asset_type is not None and asset_type not in ["satellite", "groundstation"]:
        raise HTTPException(400, detail="Invalid asset type")

    sat_names, gs_names = [],[]
    if asset_type == "satellite" or asset_type == None:
        sat_names = [res.name for res in db.query(Satellite.satellite_name).all()]
    if asset_type == "groundstation" or asset_type == None:
        gs_names = [res.name for res in db.query(GroundStation.ground_station_name).all()]

    return {"satellites": sat_names, "groundstations": gs_names}
