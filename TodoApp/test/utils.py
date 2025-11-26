import pytest
from sqlalchemy import create_engine, text
from sqlalchemy.pool import StaticPool
from sqlalchemy.orm import sessionmaker
from ..models import Base, Todos, Users
from ..main import app
from ..routers.auth import bcrypt_context
from fastapi.testclient import TestClient

SQLALCHEMY_DATABASE_URL = "sqlite:///./testdb.db"


engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

TestSessionLocal = sessionmaker(autoflush=False, autocommit=False, bind=engine)

Base.metadata.create_all(bind=engine)


def override_get_db():
    db = TestSessionLocal()
    try:
        yield db
    finally:
        db.close()


def override_get_current_user():
    return {"username": "willswinson", "user_id": 1, "user_role": "admin"}


def override_authenticate_user():
    pass


client = TestClient(app)


@pytest.fixture
def test_todo():
    todo = Todos(
        title="Learn to code!",
        priority=3,
        description="Need to learn everyday!",
        complete=False,
        user_id=1,
    )

    db = TestSessionLocal()

    db.add(todo)
    db.commit()

    yield todo
    with engine.connect() as connection:
        connection.execute(text("DELETE FROM todos;"))
        connection.commit()


@pytest.fixture
def test_user():
    user = Users(
        username="willswinson",
        email="ws@gmail.com",
        phone_number="213-234-3344",
        role="admin",
        first_name="will",
        last_name="swinson",
        hash_password=bcrypt_context.hash("test"[:72]),
        is_active=True,
    )

    db = TestSessionLocal()

    db.add(user)
    db.commit()

    yield user
    with engine.connect() as connection:
        connection.execute(text("DELETE FROM users;"))
        connection.commit()
