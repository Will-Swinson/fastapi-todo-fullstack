from .utils import *
from ..routers.auth import (
    get_db,
    authenticate_user,
    create_access_token,
    get_current_user,
    ALGORITHM,
    SECRET_KEY,
)
from datetime import timedelta, datetime, timezone
from jose import jwt
import pytest
from fastapi import HTTPException, status

app.dependency_overrides[get_db] = override_get_db


def test_authenticate_user(test_user):
    db = TestSessionLocal()

    authenticated_user = authenticate_user(test_user.username, "test", db)

    assert authenticated_user is not None

    assert authenticated_user.username == test_user.username

    non_existent_user = authenticate_user("wrong_username", "test", db)

    assert non_existent_user is False

    invalid_password = authenticate_user(test_user.username, "wrong_password", db)

    assert invalid_password is False


def test_create_access_token():
    username = "fake_username"
    role = "fake_role"
    id = 1

    token = create_access_token(username, id, role, timedelta(minutes=20))

    assert token is not None

    decoded_token = jwt.decode(
        token, SECRET_KEY, algorithms=[ALGORITHM], options={"verify_signature": False}
    )

    assert decoded_token["sub"] == username
    assert decoded_token["id"] == id
    assert decoded_token["role"] == role


@pytest.mark.asyncio
async def test_get_current_user():
    encode = {
        "sub": "test_user",
        "id": 1,
        "role": "user",
        "exp": datetime.now(timezone.utc) + timedelta(minutes=20),
    }

    token = jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)

    user = await get_current_user(token)

    assert user == {"user_id": 1, "user_role": "user", "username": "test_user"}


@pytest.mark.asyncio
async def test_get_current_user_missing_payload():
    encode = {
        "role": "user",
    }

    token = jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)

    with pytest.raises(HTTPException) as excinfo:
        await get_current_user(token)

    assert excinfo.value.status_code == status.HTTP_401_UNAUTHORIZED
    assert excinfo.value.detail == "Could not Authenticate"
