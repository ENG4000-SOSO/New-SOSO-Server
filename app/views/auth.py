from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from typing import Annotated, Optional
from sqlalchemy.orm import Session
from starlette import status
from app.db.connection import get_db
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from jose import jwt, JWTError
from datetime import timedelta, datetime, timezone
from app.models.users import Users
import logging

# Set up logging for auth module
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

router = APIRouter(
    prefix='/auth',
    tags=['auth']
)

# SECRET_KEY and ALGORITHM for JWT encoding. In production, load SECRET_KEY from env vars.
SECRET_KEY = '860314f05d3da574e14f7ffd927250eed05224b7aa7617f2a7b2a9f93e3153ba'
ALGORITHM = 'HS256'

# Create a CryptContext instance for hashing and verifying passwords.
bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
oauth2_bearer = OAuth2PasswordBearer(tokenUrl='auth/token')

# Pydantic model for user registration
class CreateUserRequest(BaseModel):
    username: str = Field(..., description="Unique username")
    first_name: str = Field(..., description="User's first name")
    last_name: str = Field(..., description="User's last name")
    email: str = Field(..., description="User's email address")
    password: str = Field(..., description="User's password")
    role: Optional[str] = Field("viewer", description="User role; defaults to viewer")
    is_active: Optional[bool] = Field(True, description="Is the user active?")

# Pydantic model for token response
class Token(BaseModel):
    access_token: str
    token_type: str

db_dependency = Annotated[Session, Depends(get_db)]

def authenticate_user(username: str, password: str, db: Session):
    """
    Authenticate a user by verifying the username and password.
    Returns the user if authentication succeeds, or False otherwise.
    """
    user = db.query(Users).filter(Users.username == username).first()
    if not user:
        logger.info("Authentication failed: user '%s' not found", username)
        return False
    if not bcrypt_context.verify(password, user.hashed_password):
        logger.info("Authentication failed: incorrect password for '%s'", username)
        return False
    logger.info("User '%s' authenticated successfully", username)
    return user

def create_access_token(username: str, user_id: int, role: str, expires_delta: timedelta):
    """
    Generate a JWT access token for the given user details.
    """
    payload = {'name': username, 'id': user_id, 'role': role}
    expires = datetime.now(timezone.utc) + expires_delta
    payload.update({'exp': expires})
    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    logger.info("Access token created for user '%s'", username)
    return token

async def get_current_user(token: Annotated[str, Depends(oauth2_bearer)]):
    """
    Decode the JWT token and return current user details.
    Raises an HTTP 401 exception if token is invalid or expired.
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get('name')
        user_id: int = payload.get('id')
        user_role: str = payload.get('role')
        if username is None or user_id is None:
            logger.error("JWT payload missing 'name' or 'id'")
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Could not validate user.')
        return {'username': username, 'id': user_id, 'user_role': user_role}
    except JWTError as e:
        logger.error("JWT decoding error: %s", e)
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Could not validate user.')

# Role-check dependencies
def admin_required(current_user: dict = Depends(get_current_user)):
    if current_user.get('user_role') != "admin":
        logger.warning("User '%s' does not have admin privileges", current_user.get('username'))
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Admin access required")
    return True

def operator_required(current_user: dict = Depends(get_current_user)):
    if current_user.get('user_role') != "operator":
        logger.warning("User '%s' does not have operator privileges", current_user.get('username'))
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Operator access required")
    return True

def viewer_required(current_user: dict = Depends(get_current_user)):
    if current_user.get('user_role') != "viewer":
        logger.warning("User '%s' does not have viewer privileges", current_user.get('username'))
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Viewer access required")
    return True

@router.post("/", status_code=status.HTTP_201_CREATED)
async def register_user(db: db_dependency, create_user_request: CreateUserRequest):
    """
    Register a new user. Checks for duplicate username or email before creation.
    """
    logger.info("Attempting to register user: %s", create_user_request.username)
    
    # Check for existing username
    existing_user = db.query(Users).filter(Users.username == create_user_request.username).first()
    if existing_user:
        logger.warning("Registration failed: username '%s' already exists", create_user_request.username)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username already exists")
    
    # Check for existing email
    existing_email = db.query(Users).filter(Users.email == create_user_request.email).first()
    if existing_email:
        logger.warning("Registration failed: email '%s' already exists", create_user_request.email)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already exists")
    
    try:
        create_user_model = Users(
            username=create_user_request.username,
            first_name=create_user_request.first_name,
            last_name=create_user_request.last_name,
            email=create_user_request.email,
            hashed_password=bcrypt_context.hash(create_user_request.password),
            role=create_user_request.role or "viewer",
            is_active=create_user_request.is_active if create_user_request.is_active is not None else True
        )
        logger.info("Adding user '%s' to the database", create_user_request.username)
        db.add(create_user_model)
        db.commit()
        db.refresh(create_user_model)
        logger.info("User '%s' registered successfully", create_user_request.username)
        return {"message": "User registered successfully"}
    except Exception as e:
        db.rollback()
        logger.error("Registration error for user '%s': %s", create_user_request.username, e)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Registration failed")

@router.post("/token", response_model=Token)
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: db_dependency):
    """
    Log in a user and return a JWT access token.
    Expects username and password as form data.
    """
    logger.info("Login attempt for user: %s", form_data.username)
    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        logger.warning("Login failed for user: %s", form_data.username)
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Could not validate user.')
    token = create_access_token(user.username, user.id, user.role, timedelta(minutes=20))
    logger.info("Login successful for user: %s", user.username)
    return {'access_token': token, 'token_type': 'bearer'}