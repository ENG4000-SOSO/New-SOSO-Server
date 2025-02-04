from app.db.base import Base
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.types import Enum

class Users(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True)
    first_name = Column(String)
    last_name = Column(String)
    email = Column(String, unique=True)
    hashed_password = Column(String)
    role = Column(Enum('admin', 'operator', 'viewer', name='user_roles'), default='viewer')
    is_active = Column(Boolean, default=True)
    
    