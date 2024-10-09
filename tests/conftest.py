import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.database import Base
from app.dependencies import get_db
from app.main import app
from app.config import settings
from app.models import User
from auth.dependencies import get_current_user

# Define the test database engine
SQLALCHEMY_TEST_DATABASE_URL = f"postgresql+psycopg2://{settings.db_user}:{settings.db_password}@{settings.db_host}:{settings.db_port}/{settings.test_db_name}"

# Create the test database engine
engine = create_engine(SQLALCHEMY_TEST_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create a TestClient to send requests to the FastAPI
client = TestClient(app)


# Override for test database
def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


# Override the default get_db dependency to use the test database
app.dependency_overrides[get_db] = override_get_db


@pytest.fixture(scope="function", autouse=True)
def setup_and_teardown():
    """
    Fixture to set up and tear down the test database.
    """
    # Setup: Clear the test database
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield
    # Teardown: Clear the test database after each test
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def create_user():
    """
    Fixture to create a user for testing.
    Returns the access token for the created user.
    """
    user_data = {
        "username": "testuser",
        "first_name": "FirstName",
        "last_name": "LastName",
        "password": "testpassword"
    }

    # Create user
    client.post("/auth/signup", json=user_data)

    # Log in to get access token
    login_response = client.post(
        "/auth/token",
        data={"username": user_data["username"], "password": user_data["password"]}
    )
    assert login_response.status_code == 200
    access_token = login_response.json()["access_token"]

    return access_token


@pytest.fixture
def create_task(create_user):
    """
    Fixture to create a task for testing.
    Returns the task ID and data.
    """

    task_data = {
        "title": "Test Task",
        "description": "This is a test task.",
        "status": "New"
    }
    response = client.post("/tasks/", json=task_data, headers={"Authorization": f"Bearer {create_user}"})
    assert response.status_code == 201
    return response.json()
