from fastapi import APIRouter, Depends, HTTPException, Path
from app.models.users import Users
from app.db.connection import SessionLocal, get_db
from typing import Annotated
from starlette import status
from .auth import get_current_user, admin_required
from sqlalchemy.orm import Session

router = APIRouter(
    prefix='/admin',
    tags=['admin']
)

db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]
admin_dependency = Annotated[bool, Depends(admin_required)]


@router.get("/users", status_code=status.HTTP_200_OK)
def fetch_all_users(db: db_dependency, admin: admin_dependency):
    users = db.query(Users).all()
    return {"users": users}


@router.put("/users/{id}/role", status_code=status.HTTP_204_NO_CONTENT)
def change_user_role(user_id: int , new_role: str, db: db_dependency,admin: admin_dependency):
    user = db.query(Users).filter(Users.id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    if new_role not in ["admin", "operator", "viewer"]:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid role")
    
    user.role = new_role
    db.commit()
    db.refresh(user)
    
    
@router.delete("/users/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user_account(user_id: int, db: db_dependency, admin: admin_dependency):
    user = db.query(Users).filter(Users.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(user)
    db.commit()
    