from typing import Optional

from pydantic import BaseModel

class CreateUserRequest(BaseModel):
    username: str
    first_name: str
    last_name: str
    email: str
    password: str
    role: Optional[str] = "viewer"
    is_active: Optional[bool] = True

class LoginRequest(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str
