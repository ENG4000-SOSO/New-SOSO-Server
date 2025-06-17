from datetime import timedelta, datetime, timezone
from typing import Annotated

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from starlette import status

from app.db.connection import get_db
from app.models.users import Users


SECRET_KEY = '860314f05d3da574e14f7ffd927250eed05224b7aa7617f2a7b2a9f93e3153ba'
ALGORITHM = 'HS256'

bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
oauth2_bearer = OAuth2PasswordBearer(tokenUrl='auth/token')

db_dependency = Annotated[Session, Depends(get_db)]

def authenticate_user(username: str, password: str, db: db_dependency):
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
        username: str | None = payload.get('name')
        user_id: int | None = payload.get('id')
        user_role: str | None = payload.get('role')
        if username is None or user_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Could not validate user.')
        return {'username': username, 'id': user_id, 'role': user_role}
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Could not validate user.')

# Add method to check admin role
def admin_required(current_user: Users = Depends(get_current_user)):
    print(current_user.get('role'))
    print(1)
    if current_user.get('role') != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Admin access required")
    return True

# Add method to check operator role
def operator_required(current_user: Users = Depends(get_current_user)):
    print(current_user.get('role'))
    print(2)
    if current_user.get('role') not in ["operator", "admin"]:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Operator access required")
    return True

# Add method to check viewer role
def viewer_required(current_user: Users = Depends(get_current_user)):
    if current_user.get('role') != "viewer":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Viewer access required")
    return True

user_dependency = Annotated[dict, Depends(get_current_user)]

operator_dependency = Annotated[bool, Depends(operator_required)]
