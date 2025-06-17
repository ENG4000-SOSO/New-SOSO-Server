import os
from sqlalchemy import create_engine
from sqlalchemy.engine.url import URL
from sqlalchemy.orm import sessionmaker


def get_env_var(name: str) -> str:
    value = os.getenv(name)
    if value is None:
        raise RuntimeError(f"Missing required environment variable: {name}")
    return value


DATABASE_CONFIG = {
    "drivername": "postgresql",
    "username": get_env_var("POSTGRES_USER"),
    "password": get_env_var("POSTGRES_PASSWORD"),
    "host": get_env_var("POSTGRES_HOST"),
    "port": int(get_env_var("POSTGRES_PORT")),
    "database": get_env_var("POSTGRES_DB"),
}

SQLALCHEMY_DATABASE_URL = str(URL.create(**DATABASE_CONFIG))

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
