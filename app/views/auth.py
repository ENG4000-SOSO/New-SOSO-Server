from datetime import timedelta
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from starlette import status

from app.models.users import Users
from app.utils.auth import authenticate_user, bcrypt_context, create_access_token, db_dependency
from app.views.dto.auth import CreateUserRequest, Token, LoginRequest

router = APIRouter(
    prefix='/auth',
    tags=['auth']
)

@router.post("/", status_code=status.HTTP_201_CREATED)
async def register_user(db: db_dependency, create_user_request: CreateUserRequest):
    create_user_model = Users(
        username = create_user_request.username,
        first_name = create_user_request.first_name,
        last_name = create_user_request.last_name,
        email = create_user_request.email,
        hashed_password = bcrypt_context.hash(create_user_request.password),
        role = create_user_request.role or "viewer",
        is_active= create_user_request.is_active if create_user_request.is_active is not None else True
    )
    db.add(create_user_model)
    db.commit()

@router.post("/token", response_model=Token)
async def login_for_access_token(form_data: LoginRequest, db: db_dependency):
    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Could not validate user.')
    token = create_access_token(user.username, user.id, user.role, timedelta(days=30))
    return {'access_token': token, 'token_type': 'bearer'}
