from fastapi import APIRouter, status, Depends, HTTPException, Request
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from pydantic import BaseModel
from ..database import SessionLocal
from sqlalchemy.orm import Session
from typing import Annotated
from datetime import timedelta, datetime, timezone
from ..models import Users
from passlib.context import CryptContext
from jose import jwt, JWTError
from fastapi.templating import Jinja2Templates

SECRET_KEY = "a9019630bcb4de783ca3cb447e00259227b9c9310b4f74f080decb262d9c38a0"
ALGORITHM = "HS256"

router = APIRouter(prefix="/auth", tags=["auth"])

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_bearer = OAuth2PasswordBearer(tokenUrl="auth/token")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_deps = Annotated[Session, Depends(get_db)]


class Token(BaseModel):
    access_token: str
    type: str


class CreateUserRequest(BaseModel):
    model_config = {
        "json_schema_extra": {
            "example": {
                "username": "willswinson",
                "email": "ws@email.com",
                "first_name": "Will",
                "last_name": "Swinson",
                "password": "P@SSWORD",
                "phone_number": "912-232-1121",
                "role": "admin",
            }
        }
    }

    username: str
    email: str
    phone_number: str
    first_name: str
    last_name: str
    password: str
    role: str


templates = Jinja2Templates(directory="TodoApp/templates")


# Pages
@router.get("/login-page")
def render_login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


@router.get("/register-page")
def render_register_page(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})


# Endpoints
def authenticate_user(username: str, password: str, db: db_deps):
    user = db.query(Users).filter(Users.username == username).first()

    if not user:
        return False

    is_valid_password = bcrypt_context.verify(password, user.hash_password)

    if not is_valid_password:
        return False

    return user


def create_access_token(
    username: str, user_id: int, role: str, expires_delta: timedelta
):
    encode = {"sub": username, "id": user_id, "role": role}
    expires = datetime.now(timezone.utc) + expires_delta
    encode.update({"exp": expires})

    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)


async def get_current_user(token: Annotated[str, Depends(oauth2_bearer)]):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        user_id: int = payload.get("id")
        user_role: str = payload.get("role")

        if not username or not user_id:
            raise HTTPException(status_code=401, detail="Could not Authenticate")

        return {"username": username, "user_id": user_id, "user_role": user_role}
    except JWTError:
        raise HTTPException(status_code=401, detail="Could not Authenticate")


@router.get("/", status_code=status.HTTP_200_OK)
async def get_user(db: db_deps):
    return db.query(Users).all()


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_user(db: db_deps, user_request: CreateUserRequest):
    try:
        encrypted_pass = bcrypt_context.hash(user_request.password)

        user_model = Users(
            email=user_request.email,
            phone_number=user_request.phone_number,
            username=user_request.username,
            first_name=user_request.first_name,
            last_name=user_request.last_name,
            hash_password=encrypted_pass,
            role=user_request.role,
            is_active=True,
        )

        db.add(user_model)
        db.commit()
    except:
        raise HTTPException(status_code=404, detail="User not created")


@router.post("/token", response_model=Token, status_code=status.HTTP_200_OK)
async def login_for_token(
    db: db_deps, form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
):
    user = authenticate_user(form_data.username, form_data.password, db)

    if not user:
        raise HTTPException(status_code=401, detail="Could not Authenticate")

    token = create_access_token(
        user.username, user.id, user.role, timedelta(minutes=20)
    )

    return {"access_token": token, "type": "bearer"}
