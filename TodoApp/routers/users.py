from fastapi import APIRouter, Depends, HTTPException, status, Path
from pydantic import BaseModel, Field
from typing import Annotated, Optional
from sqlalchemy.orm import Session
from ..models import Users
from ..database import SessionLocal
from .auth import get_current_user, bcrypt_context

router = APIRouter(prefix="/users", tags=["users"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class ChangePasswordRequest(BaseModel):
    model_config = {
        "json_schema_extra": {
            "example": {
                "current_password": "CURRENT_PASS",
                "new_password": "NEW_P@SSWORD",
            }
        }
    }

    current_password: str
    new_password: str


class UpdatePhoneNumberRequest(BaseModel):
    model_config = {
        "json_schema_extra": {"example": {"new_phone_number": "423-433-1212"}}
    }

    new_phone_number: str


db_deps = Annotated[Session, Depends(get_db)]
user_deps = Annotated[dict, Depends(get_current_user)]


@router.get("/current_user", status_code=status.HTTP_200_OK)
async def get_user(user: user_deps, db: db_deps):
    return db.query(Users).filter(Users.id == user.get("user_id")).first()


@router.put("/change_password", status_code=status.HTTP_204_NO_CONTENT)
async def change_password(
    user: user_deps, db: db_deps, password_request: ChangePasswordRequest
):
    user_model = db.query(Users).filter(Users.id == user.get("user_id")).first()

    if user_model is None:
        raise HTTPException(status_code=404, detail="Could not find user")

    is_valid_password = bcrypt_context.verify(
        password_request.current_password, user_model.hash_password
    )

    if not is_valid_password:
        raise HTTPException(
            status_code=404, detail="Could not validate current password"
        )

    encrypted_pass = bcrypt_context.hash(password_request.new_password)

    user_model.hash_password = encrypted_pass

    db.add(user_model)
    db.commit()


@router.put("/update_phone_number", status_code=status.HTTP_204_NO_CONTENT)
async def update_phone_number(
    user: user_deps, db: db_deps, update_request: UpdatePhoneNumberRequest
):
    user_model = db.query(Users).filter(Users.id == user.get("user_id")).first()

    if user_model is None:
        raise HTTPException(status_code=404, detail="Could not find user")

    user_model.phone_number = update_request.new_phone_number

    db.add(user_model)
    db.commit()
