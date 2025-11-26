from .utils import *
from ..routers.admin import get_current_user, get_db
from fastapi import status

app.dependency_overrides[get_current_user] = override_get_current_user
app.dependency_overrides[get_db] = override_get_db


def test_admin_read_all_todos(test_todo):
    response = client.get("/admin/todo")

    assert response.status_code == status.HTTP_200_OK

    assert response.json() == [
        {
            "id": 1,
            "title": "Learn to code!",
            "priority": 3,
            "description": "Need to learn everyday!",
            "complete": False,
            "user_id": 1,
        }
    ]


def test_admin_delete_todo(test_todo):
    response = client.delete("/admin/todo/delete/1")

    assert response.status_code == status.HTTP_204_NO_CONTENT

    db = TestSessionLocal()

    model = db.query(Todos).filter(Todos.id == 1).first()

    assert model is None


def test_admin_delete_todo_not_found():
    response = client.delete("/admin/todo/delete/999")

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {"detail": "Todo Not Found"}
