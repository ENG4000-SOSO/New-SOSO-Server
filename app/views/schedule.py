from datetime import datetime
import json
import logging
import os
from typing import cast
import uuid

import boto3
from mypy_boto3_dynamodb.service_resource import DynamoDBServiceResource
from mypy_boto3_ecs.client import ECSClient
from mypy_boto3_s3.client import S3Client
from fastapi import APIRouter, HTTPException, Response, status
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from sqlalchemy import Column

from app.models.assets import Satellite, GroundStation
from app.models.imaging import ImageRequest
from app.models.schedule import ScheduleRequest
from app.utils.auth import db_dependency, user_dependency, operator_dependency
from app.views.dto.schedule import \
    convert_priority, \
    GenerateScheduleRequestDto, \
    GroundStation as GS, \
    Job, \
    ScheduleParameters, \
    SchedulingInputOutputData, \
    TwoLineElement


logger = logging.getLogger(__name__)

router = APIRouter(
    prefix='/schedule',
    tags=['schedule']
)

def get_and_refresh_schedule(db: db_dependency, id: uuid.UUID):
    order = db.query(ScheduleRequest).filter(ScheduleRequest.id == id).one()

    if str(order.status).lower().strip() != 'completed':
        logger.info(f'Refreshing schedule request {id} from DynamoDb')

        dynamodb: DynamoDBServiceResource = cast(
            DynamoDBServiceResource,
            boto3.resource('dynamodb', region_name=os.getenv('AWS_REGION_NAME', 'us-east-1'))
        )

        table = dynamodb.Table(os.getenv('DYNAMODB_TABLE_NAME', 'soso-schedule-metadata'))
        response = table.get_item(Key={'job_id': str(id)})
        job_metadata = response.get('Item')

        if job_metadata is None:
            raise Exception(f'Job metadata with id {id} does not exist')

        if 'created_at' in job_metadata:
            order.created_at = cast(
                Column[datetime],
                datetime.fromisoformat(str(job_metadata['created_at']))
            )
        if 'updated_at' in job_metadata:
            order.updated_at = cast(
                Column[datetime],
                datetime.fromisoformat(str(job_metadata['updated_at']))
            )
        if 'input_object_key' in job_metadata:
            order.input_object_key = cast(
                Column[str],
                str(job_metadata['input_object_key'])
            )
        if 'output_object_key' in job_metadata:
            order.output_object_key = cast(
                Column[str],
                str(job_metadata['output_object_key'])
            )
        if 'status' in job_metadata:
            order.status = cast(
                Column[str],
                str(job_metadata['status'])
            )

        db.commit()
        db.refresh(order)

    return order


@router.post("/generate")
async def generate_schedule(db: db_dependency, user: user_dependency, operator: operator_dependency, request: GenerateScheduleRequestDto):
    logger.info('Received schedule request')

    # Step 1: Get data from database
    satellites = db.query(Satellite).filter(Satellite.id.in_(request.satellite_ids)).all()
    ground_stations = db.query(GroundStation).filter(GroundStation.id.in_(request.ground_station_ids)).all()
    imaging_requests = db.query(ImageRequest).filter(ImageRequest.id.in_(request.image_request_ids)).all()

    two_line_elements = [
        TwoLineElement(
            name=cast(str, satellite.satellite_name),
            line1=cast(str, satellite.tle_line1),
            line2=cast(str, satellite.tle_line2)
        )
        for satellite in satellites
    ]

    gs = [
        GS(
            name=cast(str, ground_station.ground_station_name),
            latitude=cast(float, ground_station.latitude),
            longitude=cast(float, ground_station.longitude),
            height=cast(float, ground_station.elevation),
            mask=cast(int, ground_station.send_mask),
            uplink_rate=cast(int, ground_station.uplink_rate),
            downlink_rate=cast(int, ground_station.downlink_rate)
        )
        for ground_station in ground_stations
    ]

    jobs = [
        Job(
            name=cast(str, imaging_request.image_name),
            latitude=cast(float, imaging_request.latitude),
            longitude=cast(float, imaging_request.longitude),
            priority=convert_priority(cast(int, imaging_request.priority)),
            start=cast(datetime, imaging_request.image_start_time),
            end=cast(datetime, imaging_request.image_end_time),
            delivery=cast(datetime, imaging_request.delivery_time)
        )
        for imaging_request in imaging_requests
    ]

    # Step 2: Build parameters object
    params = ScheduleParameters(
        input_hash="",
        two_line_elements=two_line_elements,
        jobs=jobs,
        ground_stations=gs,
        outage_requests=[],
        ground_station_outage_requests=[]
    )

    # Step 3: Make schedule request
    logger.info('Making schedule request')
    schedule_request = ScheduleRequest(
        id=uuid.uuid4(),
        mission_id=request.mission_id,
        created_at=datetime.now().isoformat(),
        updated_at=datetime.now().isoformat(),
        status='started'
    )

    # Step 4: Store schedule request in database
    db.add(schedule_request)
    db.commit()

    # Step 5: Store parameters in S3
    logger.info('Storing parameters in S3')

    s3: S3Client = cast(S3Client, boto3.client('s3'))

    data = json.dumps(params.model_dump_json(), sort_keys=True)
    object_key = f'input/{str(schedule_request.id)}.json'

    s3.put_object(
        Bucket=os.getenv('S3_BUCKET_NAME', 'soso-storage'),
        Key=object_key,
        Body=data,
        ContentType='application/json'
    )

    # Step 6: Store schedule request in DynamoDb
    logger.info('Storing schedule request in DynamoDb')
    dynamodb: DynamoDBServiceResource = cast(
        DynamoDBServiceResource,
        boto3.resource('dynamodb', region_name=os.getenv('AWS_REGION_NAME', 'us-east-1'))
    )
    table = dynamodb.Table(os.getenv('DYNAMODB_TABLE_NAME', 'soso-schedule-metadata'))
    table.put_item(Item={
        'job_id': str(schedule_request.id),
        'status': 'started',
        'input_object_key': object_key,
        'created_at': datetime.now().isoformat(),
        'updated_at': datetime.now().isoformat()
    })

    # Step 7: Start scheduler
    logger.info('Starting scheduler')
    ecs = cast(ECSClient, boto3.client('ecs'))

    task_definition_name = 'soso-task-1-0-2'
    container_name = 'soso-ecr-1-0-2'

    response = ecs.run_task(
        cluster='soso-cluster',
        taskDefinition=task_definition_name,
        launchType='FARGATE',
        count=1,
        platformVersion='LATEST',
        networkConfiguration={
            'awsvpcConfiguration': {
                'subnets': [
                    'subnet-065b7ba836bb8abe4',
                    'subnet-07c8e866355241b55',
                    'subnet-07bec1e0c96c7c843',
                    'subnet-04c70d8c155d1a70f',
                    'subnet-0d08600835610c833',
                    'subnet-05ca5bacdb1f96f26'
                ],
                'securityGroups': ['sg-03ad89ab0d6f6eb67'],
                'assignPublicIp': 'ENABLED'
            }
        },
        overrides={
            'containerOverrides': [{
                'name': container_name,
                'environment': [
                    {
                        'name': 'JOB_ID',
                        'value': str(schedule_request.id)
                    }
                ]
            }]
        }
    )

    if response['failures']:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        return JSONResponse(status_code=status.HTTP_202_ACCEPTED, content={'job_id': str(schedule_request.id)})


@router.get("/mission/{id}")
async def get_schedules_by_mission(db: db_dependency, user: user_dependency, id: int):
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication Failed')

    orders = db.query(ScheduleRequest).filter(ScheduleRequest.mission_id == id).all()

    return JSONResponse(status_code=status.HTTP_200_OK, content=jsonable_encoder(orders))


@router.get("/{id}")
async def get_schedule_by_id(db: db_dependency, user: user_dependency, id: uuid.UUID):
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication Failed')

    order = get_and_refresh_schedule(db, id)

    status_code = status.HTTP_200_OK if str(order.status).lower().strip() == 'completed' else status.HTTP_202_ACCEPTED
    return JSONResponse(status_code=status_code, content=jsonable_encoder(order))


@router.get("/output/{id}")
async def get_schedule_output_by_id(db: db_dependency, user: user_dependency, id: uuid.UUID):
    order = get_and_refresh_schedule(db, id)

    if str(order.status).lower().strip() != 'completed':
        return Response(status_code=status.HTTP_202_ACCEPTED)

    object_key = str(order.output_object_key)
    logger.info(f'Retrieving {object_key} from S3 bucket {os.getenv('S3_BUCKET_NAME', 'soso-storage')}')

    s3: S3Client = cast(S3Client, boto3.client('s3'))
    response = s3.get_object(
        Bucket=os.getenv('S3_BUCKET_NAME', 'soso-storage'),
        Key=object_key
    )

    data = json.loads(response['Body'].read())

    return SchedulingInputOutputData.model_validate_json(data)
