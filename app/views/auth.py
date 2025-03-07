from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import Annotated, Optional
from sqlalchemy.orm import Session
from starlette import status
from app.db.connection import SessionLocal, get_db
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from jose import jwt, JWTError
from datetime import timedelta, datetime, timezone
from app.models.users import Users



router = APIRouter(
    prefix='/auth',
    tags=['auth']
)

SECRET_KEY = '860314f05d3da574e14f7ffd927250eed05224b7aa7617f2a7b2a9f93e3153ba'
ALGORITHM = 'HS256'

bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
oauth2_bearer = OAuth2PasswordBearer(tokenUrl='auth/token')

class CreateUserRequest(BaseModel):
    username: str
    first_name: str
    last_name: str
    email: str
    password: str
    role: Optional[str] = "viewer"  # Default to 'viewer'
    is_active: Optional[bool] = True  # Default to True

class Token(BaseModel):
    access_token: str
    token_type: str

db_dependency = Annotated[Session, Depends(get_db)]

def authenticate_user(username: str, password: str, db):
    user = db.query(Users).filter(Users.username == username).first()
    if not user:
        return False
    if not bcrypt_context.verify(password, user.hashed_password):
        return False
    return user

def create_access_token(username: str, user_id: int, role: str, expires_delta: timedelta):
    encode = {'name': username, 'id': user_id, 'role': role}
    expires = datetime.now(timezone.utc) + expires_delta
    encode.update({'exp': expires})
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)

async def get_current_user(token: Annotated[str, Depends(oauth2_bearer)]):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get('name')
        user_id: int = payload.get('id')
        user_role: str = payload.get('role')
        if username is None or user_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Could not validate user.')
        return {'username': username, 'id': user_id, 'user_role': user_role}
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Could not validate user.')
    
# Add method to check admin role
def admin_required(current_user: Users = Depends(get_current_user)):
    if current_user.get('user_role') != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Admin access required")
    return True

# Add method to check operator role
def operator_required(current_user: Users = Depends(get_current_user)):
    if current_user.get('user_role') != "operator":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Operator access required")
    return True

# Add method to check viewer role
def viewer_required(current_user: Users = Depends(get_current_user)):
    if current_user.get('user_role') != "viewer":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Viewer access required")
    return True

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
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: db_dependency):
    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Could not validate user.')
    token = create_access_token(user.username, user.id, user.role, timedelta(minutes=20))
    return {'access_token': token, 'token_type': 'bearer'}


