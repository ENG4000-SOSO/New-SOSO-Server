"""
This module defines the Users model for application users.
Each user has a username, name details, email, hashed password, a role, and an active status.
The role is implemented as an ENUM, which is defined in the database schema.
"""

from app.db.base import Base
from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.types import Enum

class Users(Base):
    """
    Users model represents an application user with authentication and authorization details.
    """
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False)  # Unique username, cannot be NULL
    first_name = Column(String, nullable=False)             # First name should be provided
    last_name = Column(String, nullable=False)              # Last name should be provided
    email = Column(String, unique=True, nullable=False)       # Unique email, cannot be NULL
    hashed_password = Column(String, nullable=False)          # Password must be hashed; required field
    # Use the ENUM type 'user_roles' defined in the database. The default is "viewer".
    role = Column(Enum('admin', 'operator', 'viewer', name='user_roles'), default='viewer', nullable=False)
    is_active = Column(Boolean, default=True)                 # Indicates if the account is active

    def __repr__(self):
        return f"<User(id={self.id}, username='{self.username}', role='{self.role}')>"