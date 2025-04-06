import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Use an environment variable for the database URL; fallback to default if not set
SQLALCHEMY_DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://postgres:test1234@localhost/SOSOApplicationDatabase"
)

# Create the SQLAlchemy engine
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# Create a configured "Session" class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    """
    Dependency function that creates a new SQLAlchemy session,
    yields it for use in a request, and ensures it is closed after.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()