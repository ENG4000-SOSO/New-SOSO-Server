from pydantic import BaseModel

from app.views.dto.window import Window


class OutageOrderCreationRequestDto(BaseModel):
    Target: str
    Activity: str
    Window: Window
