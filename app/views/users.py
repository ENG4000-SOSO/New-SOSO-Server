from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from app.models.users import Users
from app.db.connection import get_db
from typing import Annotated
from starlette import status
from passlib.context import CryptContext
from .auth import get_current_user
from sqlalchemy.orm import Session
import logging

# Set up logging for users module
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

router = APIRouter(
    prefix='/user',
    tags=['user']
)

db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]
bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

class UserVerification(BaseModel):
    """
    Model for verifying a user's password and specifying a new password.
    """
    password: str
    new_password: str = Field(..., min_length=6, description="New password must be at least 6 characters long")

@router.get('/', status_code=status.HTTP_200_OK)
async def get_user_details(user: user_dependency, db: db_dependency):
    """
    Retrieve the details of the currently authenticated user.
    """
    if user is None:
        logger.warning("Unauthorized access attempt to get user details")
        raise HTTPException(status_code=401, detail='Authentication Failed')
    db_user = db.query(Users).filter(Users.id == user.get('id')).first()
    if not db_user:
        logger.error("User with id %s not found", user.get('id'))
        raise HTTPException(status_code=404, detail='User not found')
    logger.info("Fetched details for user: %s", db_user.username)
    return db_user

@router.put("/password", status_code=status.HTTP_204_NO_CONTENT)
async def change_password(user: user_dependency, db: db_dependency, user_verification: UserVerification):
    """
    Change the password for the currently authenticated user.
    Verifies the current password before updating.
    """
    if user is None:
        logger.warning("Unauthorized access attempt to change password")
        raise HTTPException(status_code=401, detail='Authentication Failed')
    user_model = db.query(Users).filter(Users.id == user.get('id')).first()
    if not bcrypt_context.verify(user_verification.password, user_model.hashed_password):
        logger.warning("Password change failed for user '%s': incorrect current password", user.get('username'))
        raise HTTPException(status_code=401, detail='Error on password change')
    user_model.hashed_password = bcrypt_context.hash(user_verification.new_password)
    db.add(user_model)
    db.commit()
    logger.info("Password updated for user: %s", user.get('username'))