from fastapi import APIRouter, HTTPException, Query

from app.models.imaging import ImageRequest
from app.utils.api import paginated_response
from app.utils.auth import db_dependency, user_dependency, operator_dependency
from app.views.dto.imaging import CreateImageRequest


router = APIRouter(
    prefix='/imaging',
    tags=['imaging']
)


@router.post("/order")
async def create_order(db: db_dependency, user: user_dependency, operator: operator_dependency, image_request: CreateImageRequest):
    # Creates a new image order based on provided data.
    if user is None:
        raise HTTPException(status_code=401,detail='Authentication Failed')

    image_request_model = ImageRequest(
        mission_id=image_request.mission_id,
        image_name=image_request.image_name,
        latitude=image_request.latitude,
        longitude=image_request.longitude,
        priority=image_request.priority,
        image_type=image_request.image_type,
        image_start_time=image_request.image_start_time,
        image_end_time=image_request.image_end_time,
        delivery_time=image_request.delivery_time,
        recurrence_revisit=image_request.recurrence.revisit if image_request.recurrence is not None else None,
        recurrence_number_of_revisits=image_request.recurrence.number_of_revisits if image_request.recurrence is not None else None,
        recurrence_revisit_frequency=image_request.recurrence.revisit_frequency if image_request.recurrence is not None else None,
        recurrence_revisit_frequency_units=image_request.recurrence.revisit_frequency_units if image_request.recurrence is not None else None
    )
    db.add(image_request_model)
    db.commit()


@router.get("/orders")
async def get_all_image_orders(db: db_dependency, user: user_dependency, page: int = Query(1, ge=1), per_page: int = Query(20, ge=1), all: bool = Query(False)):
    # Retrieves all image orders with pagination support.
    query = db.query(ImageRequest)
    total = str(query.count())
    if not all:
        query = query.limit(per_page).offset((page - 1) * per_page)
    return paginated_response([request._asdict() for request in query.all()], total)




@router.get("/mission/{id}/orders")
async def get_imaging_orders_by_mission_id(db: db_dependency, user: user_dependency, id: int):
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication Failed')

    orders = db.query(ImageRequest).filter(ImageRequest.mission_id == id).all()

    return orders
