from pydantic import BaseModel


class Window(BaseModel):
    Start: str
    End: str
