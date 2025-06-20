from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from app.models.users import Users
from app.db.connection import SessionLocal, get_db
from typing import Annotated
from starlette import status
from passlib.context import CryptContext
from app.utils.auth import get_current_user
from sqlalchemy.orm import Session

router = APIRouter(
    prefix='/user',
    tags=['user']
)

db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]
bcrypt_context = CryptContext(schemes=['bcrypt'],deprecated='auto')

class UserVerification(BaseModel):
    password: str
    new_password: str = Field(min_length=6)

@router.get('/', status_code=status.HTTP_200_OK)
async def get_user_details(user: user_dependency, db: db_dependency):
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication Failed')
    return db.query(Users).filter(Users.id == user.get('id')).first()

@router.put("/password", status_code=status.HTTP_204_NO_CONTENT)
async def change_password(user: user_dependency, db: db_dependency, user_verification: UserVerification):
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication Failed')
    user_model = db.query(Users).filter(Users.id == user.get('id')).first()
    if user_model is None:
        raise HTTPException(status_code=404, detail='User not found')

    if not bcrypt_context.verify(user_verification.password, str(user_model.hashed_password)):
        raise HTTPException(status_code=401, detail='Error on password change')

    hashed_password = bcrypt_context.hash(user_verification.new_password)
    user_model = db.query(Users)\
        .filter(Users.id == user.get('id'))\
        .update({"hashed_password": hashed_password})

    db.commit()
