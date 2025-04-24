from datetime import datetime, timezone
from enum import Enum
import hashlib
import json
from typing import Dict, List, Optional

from intervaltree import Interval
from pydantic import BaseModel, ConfigDict, field_validator


class TwoLineElement(BaseModel):
    '''
    Representation of a two-line element.
    '''

    model_config = ConfigDict(frozen=True)

    name: str
    '''
    The name of the satellite represented by the two-line element.
    '''

    line1: str
    '''
    The first line of the two-line element.
    '''

    line2: str
    '''
    The second line of the two-line element.
    '''


class Priority(Enum):
    '''
    The priority of a job.
    '''

    LOW = 1
    MEDIUM = 2
    HIGH = 3


class SatellitePassLocation(BaseModel):
    '''
    Representation of a location the a satellite passes over.
    '''

    model_config = ConfigDict(frozen=True)

    name: str
    '''
    The name of the location.
    '''

    latitude: float
    '''
    The latitude of the location.
    '''

    longitude: float
    '''
    The longitude of the location.
    '''


class Job(SatellitePassLocation):
    '''
    Representation of a job that a satellite can be asked to perform.
    '''

    model_config = ConfigDict(
        frozen=True,
        json_encoders={datetime: lambda v: v.isoformat()}
    )

    priority: Priority
    '''
    The priority of the job.
    '''

    start: datetime
    '''
    The start time of the interval in which the job must be performed.
    '''

    end: datetime
    '''
    The end time of the interval in which the job must be performed.
    '''

    delivery: datetime
    '''
    The time by which the job must be delivered to a ground station.
    '''

    size: float = 128_000_000 # TODO: MAKE THIS DYNAMIC
    '''
    The size of the image in bytes.
    '''

    @field_validator('start', 'end', 'delivery', mode='after')
    @classmethod
    def ensure_start_utc(cls, v: datetime) -> datetime:
        '''
        Ensures that the start, end, and delivery times have timezone
        information.
        '''
        return v.replace(tzinfo=timezone.utc)

    def __str__(self):
        return f'{self.name} P{self.priority.value}'

    def __repr__(self) -> str:
        return str(self)

    def interval(self) -> Interval:
        return Interval(self.start, self.end, str(self))


class GroundStation(SatellitePassLocation):
    '''
    Representation of a job that a satellite can be asked to perform.
    '''

    model_config = ConfigDict(frozen=True)

    height: float
    '''
    The elevation of the ground station.
    '''

    mask: int
    '''
    The mask of the ground station.
    '''

    uplink_rate: int
    '''
    The uplink rate of the ground station in Mbps.
    '''

    downlink_rate: int
    '''
    The downlink rate of the ground station in Mbps.
    '''

    def __str__(self):
        return f'{self.name} at lat: {self.latitude}, lon: {self.longitude}, height: {self.height}'

    def __repr__(self) -> str:
        return str(self)


class OutageRequest(BaseModel):
    '''
    Representation of an outage request that renders a satellite unusable for a
    certain amount of time.
    '''

    model_config = ConfigDict(
        frozen=True,
        json_encoders={datetime: lambda v: v.isoformat()},
    )

    name: str
    '''
    The name of the outage request.
    '''

    satellite_name: str
    '''
    The name of the satellite that the outage applies to.
    '''

    start: datetime
    '''
    The start time of the outage.
    '''

    end: datetime
    '''
    The end time of the outage.
    '''

    @field_validator('start', 'end', mode='after')
    @classmethod
    def ensure_start_utc(cls, v: datetime) -> datetime:
        '''
        Ensures that the start and end times have timezone information.
        '''
        return v.replace(tzinfo=timezone.utc)

    def __str__(self):
        return f'{self.name} - {self.satellite_name}'

    def __repr__(self) -> str:
        return str(self)

    def interval(self) -> Interval:
        return Interval(self.start, self.end, str(self))


class GroundStationOutageRequest(BaseModel):
    '''
    Representation of an outage request that renders a ground station unusable
    for a certain amount of time.
    '''

    model_config = ConfigDict(
        frozen=True,
        json_encoders={datetime: lambda v: v.isoformat()},
    )

    name: str
    '''
    The name of the outage request.
    '''

    ground_station: GroundStation
    '''
    The ground station that the outage applies to.
    '''

    start: datetime
    '''
    The start time of the outage.
    '''

    end: datetime
    '''
    The end time of the outage.
    '''

    @field_validator('start', 'end', mode='after')
    @classmethod
    def ensure_start_utc(cls, v: datetime) -> datetime:
        '''
        Ensures that the start and end times have timezone information.
        '''
        return v.replace(tzinfo=timezone.utc)

    def __str__(self):
        return f'{self.name} - {self.ground_station.name}'

    def __repr__(self) -> str:
        return str(self)

    def interval(self) -> Interval:
        return Interval(self.start, self.end, str(self))


class ScheduleParameters(BaseModel):
    '''
    Representation of the parameters of the scheduling algorithm.
    '''

    input_hash: Optional[str]
    '''
    Hash of the input parameters of the previous scheduling run. Use this
    attribute only when re-scheduling, otherwise leave this as `None`.
    '''

    two_line_elements: List[TwoLineElement]
    '''
    The list of satellites to be scheduled with orders.
    '''

    jobs: List[Job]
    '''
    The orders to be scheduled into satellites.
    '''

    ground_stations: List[GroundStation]
    '''
    The ground stations than can downlink orders from satellites.
    '''

    outage_requests: List[OutageRequest]
    '''
    The outage requests that add constraints to when satellites are unavailable.
    '''

    ground_station_outage_requests: List[GroundStationOutageRequest]
    '''
    The outage requests that add constraints to when ground stations are
    unavailable.
    '''


class PlannedOrder(BaseModel):
    '''
    Representation of a planned order.
    '''

    job: Job
    '''
    The job being planned in the order.
    '''

    satellite_name: str
    '''
    The satellite that is being planned to fulfill the order.
    '''

    ground_station_name: str
    '''
    The ground station that is being planned to downlink the order.
    '''

    job_begin: datetime
    '''
    The start time of the interval in which the satellite will complete the job.
    '''

    job_end: datetime
    '''
    The end time of the interval in which the satellite will complete the job.
    '''

    downlink_begin: datetime
    '''
    The start time of the interval in which the job will be downlinked.
    '''

    downlink_end: datetime
    '''
    The end time of the interval in which the job will be downlinked.
    '''


class ScheduleOutput(BaseModel):
    '''
    A representation of the result of the entire scheduling algorithm.
    '''

    input_hash: str
    '''
    The hash of the input parameters that produced this output. Both the user
    and the scheduler should store this value to reference this scheduling run
    in the future in the case of rescheduling.
    '''

    impossible_orders: List[Job]
    '''
    Jobs that were not scheduled because they were just not possible to be
    fulfilled.
    '''

    impossible_orders_from_outages: List[Job]
    '''
    Jobs that were not scheduled because the only times they could have been
    scheduled were blocked by outages.
    '''

    impossible_orders_from_ground_stations: List[Job]
    '''
    Jobs that were not scheduled because there was a lack of availability of
    ground stations to downlink them.
    '''

    undownlinkable_orders: List[Job]
    '''
    Orders that were impossible to be downlinked.
    '''

    rejected_orders: List[Job]
    '''
    Jobs that could have been scheduled but were not as part of the optimization
    algorithm.
    '''

    planned_orders: Dict[str, List[PlannedOrder]]
    '''
    Jobs that have been successfully scheduled.
    '''

    @classmethod
    def convert_to_hash(cls, value: ScheduleParameters):
        '''
        Hashes schedule parameters to be used as a key.
        '''

        model_json_string = json.dumps(value.model_dump_json(), sort_keys=True)
        model_json_bytes = model_json_string.encode()
        model_hash = hashlib.sha256(model_json_bytes).hexdigest()
        return model_hash


class SchedulingInputOutputData(BaseModel):
    '''
    Data model holding information about a scheduling run. Includes the input
    parameters and output data, as well as the hash of the input parameters to
    be used for retrieving this data.
    '''

    params_hash: str
    '''
    Hash of the schedule parameters.
    '''

    params: ScheduleParameters
    '''
    The parameters of the scheduling run.
    '''

    output: ScheduleOutput
    '''
    The output of the scheduling run.
    '''


class GenerateScheduleRequestDto(BaseModel):
    mission_id: int
    satellite_ids: List[int]
    ground_station_ids: List[int]
    image_request_ids: List[int]


def convert_priority(priority_int: int) -> Priority:
    if priority_int == 3:
        return Priority.HIGH
    if priority_int == 2:
        return Priority.MEDIUM
    if priority_int == 1:
        return Priority.LOW
    raise Exception(f'Invalid priority {priority_int}')
