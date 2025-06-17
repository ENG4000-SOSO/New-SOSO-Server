from fastapi import APIRouter, HTTPException, Query
from starlette import status

from app.models.mission import Mission
from app.utils.api import paginated_response
from app.utils.auth import db_dependency, user_dependency, operator_dependency
from app.views.dto.mission import MissionCreateRequestDto


router = APIRouter(
    prefix='/mission',
    tags=['mission']
)


@router.post("")
async def create_mission(db: db_dependency, user: user_dependency, operator: operator_dependency, mission: MissionCreateRequestDto):
    # Creates an outage order for a specified asset.
    if user is None:
        raise HTTPException(status_code=401,detail='Authentication Failed')

    mission_model = Mission(
        mission_name=mission.mission_name,
        mission_start=mission.mission_start,
        mission_end=mission.mission_end
    )
    db.add(mission_model)
    db.commit()


@router.get("")
async def get_all_missions(db: db_dependency, user: user_dependency):
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication Failed')
    missions = db.query(Mission).all()
    return missions


@router.get("/{id}")
async def get_mission(db: db_dependency, user: user_dependency, id: int):
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication Failed')

    mission = db.query(Mission).filter(Mission.id == id).first()

    if mission is None:
        raise HTTPException(status_code=404, detail="Mission not found")

    return mission
