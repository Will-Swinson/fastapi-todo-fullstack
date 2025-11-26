from fastapi import APIRouter, Depends, HTTPException, status, Path, Request
from pydantic import BaseModel, Field
from typing import Annotated
from sqlalchemy.orm import Session
from ..models import Todos
from ..database import SessionLocal
from .auth import get_current_user
from starlette.responses import RedirectResponse
from fastapi.templating import Jinja2Templates

router = APIRouter(prefix="/todos", tags=["todos"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_deps = Annotated[Session, Depends(get_db)]
user_deps = Annotated[dict, Depends(get_current_user)]


class TodoRequest(BaseModel):
    model_config = {
        "json_schema_extra": {
            "example": {
                "title": "A new todo",
                "description": "A new description of a todo",
                "priority": 5,
                "complete": True,
            }
        }
    }

    title: str = Field(min_length=1, max_length=100)
    description: str = Field(min_length=1, max_length=100)
    priority: int = Field(ge=1, le=5)
    complete: bool


def redirect_to_login():
    redirect_response = RedirectResponse(
        url="/auth/login-page", status_code=status.HTTP_302_FOUND
    )
    redirect_response.delete_cookie("access_token")

    return redirect_response


templates = Jinja2Templates(directory="TodoApp/templates")

# Pages


@router.get("/todo-page")
async def render_todo_page(request: Request, db: db_deps):
    try:
        access_token = request.cookies.get("access_token")

        user = await get_current_user(access_token)

        if user is None:
            return redirect_to_login()

        todos = db.query(Todos).filter(Todos.user_id == user.get("user_id")).all()

        return templates.TemplateResponse(
            "todo.html", {"request": request, "todos": todos, "user": user}
        )
    except Exception:
        return redirect_to_login()


@router.get("/add-todo-page")
async def render_add_todo_page(request: Request):
    try:
        access_token = request.cookies.get("access_token")

        user = await get_current_user(access_token)

        if user is None:
            return redirect_to_login()

        return templates.TemplateResponse(
            "add-todo.html", {"request": request, "user": user}
        )
    except Exception:
        return redirect_to_login()


@router.get("/edit-todo-page/{todo_id}")
async def render_edit_todo_page(request: Request, todo_id: int, db: db_deps):
    try:
        user = await get_current_user(request.cookies.get("access_token"))

        if user is None:
            return redirect_to_login()

        todo = db.query(Todos).filter(Todos.id == todo_id).first()

        return templates.TemplateResponse(
            "edit-todo.html", {"request": request, "todo": todo, "user": user}
        )

    except:
        return redirect_to_login()


# Endpoints
@router.get("/")
async def read_all(user: user_deps, db: db_deps):
    return db.query(Todos).filter(Todos.user_id == user.get("user_id")).all()


@router.get("/todo/{id}", status_code=status.HTTP_200_OK)
async def read_todo(db: db_deps, user: user_deps, id: int = Path(gt=0)):
    todo = (
        db.query(Todos)
        .filter(Todos.id == id)
        .filter(Todos.user_id == user.get("user_id"))
        .first()
    )

    if todo is None:
        raise HTTPException(status_code=404, detail="Todo Not Found")

    return todo


@router.post("/todo/create", status_code=status.HTTP_201_CREATED)
async def create_todo(db: db_deps, user: user_deps, todo_request: TodoRequest):
    if user is None:
        raise HTTPException(status_code=401, detail="Authentication Failed")

    todo_model = Todos(**todo_request.model_dump(), user_id=user.get("user_id"))
    db.add(todo_model)
    db.commit()


@router.put("/todo/update/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_todo(
    db: db_deps, user: user_deps, todo_request: TodoRequest, id: int = Path(gt=0)
):
    todo_model = (
        db.query(Todos)
        .filter(Todos.id == id)
        .filter(Todos.user_id == user.get("user_id"))
        .first()
    )

    if todo_model is None:
        raise HTTPException(status_code=404, detail="Todo Not Found")

    todo_model.title = todo_request.title
    todo_model.description = todo_request.description
    todo_model.priority = todo_request.priority
    todo_model.complete = todo_request.complete

    db.add(todo_model)
    db.commit()


@router.delete("/todo/delete/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(db: db_deps, user: user_deps, id: int = Path(gt=0)):
    todo_model = (
        db.query(Todos)
        .filter(Todos.id == id)
        .filter(Todos.user_id == user.get("user_id"))
        .first()
    )

    if todo_model is None:
        raise HTTPException(status_code=404, detail="Todo Not Found")

    db.delete(todo_model)
    db.commit()
