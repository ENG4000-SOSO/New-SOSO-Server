from fastapi import APIRouter, HTTPException, Query
from starlette import status

from app.models.maintenance import ActivityRequest
from app.utils.api import paginated_response
from app.utils.auth import db_dependency, user_dependency, operator_dependency
from app.views.dto.maintenance import ActivityRequestDto


router = APIRouter(
    prefix='/maintenance',
    tags=['maintenance']
)


@router.post("/maintenance/orders/create")
async def create_maintenance_request(db: db_dependency, user: user_dependency, operator: operator_dependency, maintenance_request: ActivityRequestDto):
    # Creates a maintenance request for a specified satellite.
    if user is None:
        raise HTTPException(status_code=401,detail='Authentication Failed')

    maintenance_request_model = ActivityRequest(
        target=maintenance_request.Target,
        activity=maintenance_request.Activity,
        window_start=maintenance_request.Window.Start,
        window_end=maintenance_request.Window.End,
        duration=maintenance_request.Duration,
        repeat_cycle_repetition=maintenance_request.RepeatCycle.Repetition,
        repeat_cycle_frequency_minimum_gap=maintenance_request.RepeatCycle.Frequency.MinimumGap,
        repeat_cycle_frequency_maximum_gap=maintenance_request.RepeatCycle.Frequency.MinimumGap,
        payload_outage=maintenance_request.PayloadOutage
    )
    db.add(maintenance_request_model)
    db.commit()


@router.get("/maintenance/orders")
async def get_all_maintenance_orders(db: db_dependency, user: user_dependency, page: int = Query(1, ge=1), per_page: int = Query(20, ge=1), all: bool = Query(False)):
    # Retrieves all maintenance orders with pagination support.
    query = db.query(ActivityRequest)
    total = str(query.count())
    if not all:
        query = query.limit(per_page).offset((page - 1) * per_page)
    return paginated_response([request._asdict() for request in query.all()], total)
