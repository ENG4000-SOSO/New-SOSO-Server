from pydantic import BaseModel


class MissionCreateRequestDto(BaseModel):
    mission_name: str
    mission_start: str
    mission_end: str
