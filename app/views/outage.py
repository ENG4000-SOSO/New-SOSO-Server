from fastapi import APIRouter, HTTPException, Query
from starlette import status

from app.models.outage import OutageRequest
from app.utils.api import paginated_response
from app.utils.auth import db_dependency, user_dependency, operator_dependency
from app.views.dto.outage import OutageOrderCreationRequestDto


router = APIRouter(
    prefix='/maintenance',
    tags=['maintenance']
)


@router.post("/outage/orders/create")
async def create_outage(db: db_dependency, user: user_dependency, operator: operator_dependency, outage_request: OutageOrderCreationRequestDto):
    # Creates an outage order for a specified asset.
    if user is None:
        raise HTTPException(status_code=401,detail='Authentication Failed')

    outage_request_model = OutageRequest(
        target=outage_request.Target,
        activity=outage_request.Activity,
        window_start=outage_request.Window.Start,
        window_end=outage_request.Window.End
    )
    db.add(outage_request_model)
    db.commit()


@router.get("/outage/orders")
async def get_all_outage_orders(db: db_dependency, user: user_dependency, asset_type: str = Query(None), page: int = Query(1, ge=1), per_page: int = Query(20, ge=1), all: bool = Query(False)):
    # Retrieves all outage orders with optional filtering by asset type.
    query = db.query(OutageRequest)
    if asset_type:
        # Don't know if target should be used here!!!
        query = query.filter(OutageRequest.target==asset_type)
    total = query.count()
    if not all:
        query = query.limit(per_page).offset((page - 1) * per_page)
    return paginated_response([request._asdict() for request in query.all()], total)
