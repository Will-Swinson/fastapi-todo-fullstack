from fastapi import APIRouter, Depends, HTTPException, status, Path
from typing import Annotated
from sqlalchemy.orm import Session
from ..models import Todos
from ..database import SessionLocal
from .auth import get_current_user

router = APIRouter(prefix="/admin", tags=["admin"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_deps = Annotated[Session, Depends(get_db)]
user_deps = Annotated[dict, Depends(get_current_user)]


@router.get("/todo", status_code=status.HTTP_200_OK)
async def read_all(user: user_deps, db: db_deps):
    if user.get("user_role").lower() != "admin":
        raise HTTPException(status_code=404, detail="Unauthorized")

    return db.query(Todos).all()


@router.delete("/todo/delete/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(db: db_deps, user: user_deps, id: int = Path(gt=0)):
    if user.get("user_role").lower() != "admin":
        raise HTTPException(status_code=404, detail="Unauthorized")

    todo_model = db.query(Todos).filter(Todos.id == id).first()

    if todo_model is None:
        raise HTTPException(status_code=404, detail="Todo Not Found")

    db.delete(todo_model)
    db.commit()
