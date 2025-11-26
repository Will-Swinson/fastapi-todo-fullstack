from .utils import *
from ..routers.users import get_db, get_current_user
from fastapi import status

app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = override_get_current_user


def test_get_user(test_user):
    response = client.get("/users/current_user")

    assert response.status_code == status.HTTP_200_OK

    assert response.json()["username"] == "willswinson"
    assert response.json()["email"] == "ws@gmail.com"
    assert response.json()["phone_number"] == "213-234-3344"
    assert response.json()["role"] == "admin"
    assert response.json()["first_name"] == "will"
    assert response.json()["last_name"] == "swinson"
    assert response.json()["is_active"] == True


def test_change_password_success(test_user):
    request_data = {"current_password": "test", "new_password": "testpassword"}

    response = client.put("/users/change_password", json=request_data)

    assert response.status_code == status.HTTP_204_NO_CONTENT

    db = TestSessionLocal()

    model = db.query(Users).filter(Users.id == 1).first()

    assert bcrypt_context.verify(request_data.get("new_password"), model.hash_password)


def test_change_password_invalid_password(test_user):
    request_data = {"current_password": "wrong_pass", "new_password": "testpassword"}

    response = client.put("/users/change_password", json=request_data)

    assert response.status_code == status.HTTP_404_NOT_FOUND

    assert response.json() == {"detail": "Could not validate current password"}


def test_change_phone_number(test_user):
    request_data = {"new_phone_number": "111-111-1111"}

    response = client.put("/users/update_phone_number", json=request_data)

    assert response.status_code == status.HTTP_204_NO_CONTENT

    db = TestSessionLocal()

    model = db.query(Users).filter(Users.id == 1).first()

    assert model.phone_number == request_data.get("new_phone_number")
