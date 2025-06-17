from pydantic import BaseModel

from app.views.dto.window import Window


class Frequency(BaseModel):
    MinimumGap: str
    MaximumGap: str


class RepeatCycle(BaseModel):
    Frequency: Frequency
    Repetition: str


class ActivityRequestDto(BaseModel):
    Target: str
    Activity: str
    Window: Window
    Duration: str
    RepeatCycle: RepeatCycle
    PayloadOutage: str
