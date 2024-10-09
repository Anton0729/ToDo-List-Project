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


# Override for test database
def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


# Override the default get_db dependency to use the test database
app.dependency_overrides[get_db] = override_get_db


"""
Using a mock for authentication in tests simplifies and speeds up testing by bypassing real authentication processes. 
It isolates tests from the authentication system. Mocks provide predictable responses, allowing you to focus on 
testing specific application logic without the complexities of actual authentication mechanisms.
"""


# Mock the get_current_user dependency to always return a test user
def override_get_current_user():
    return User(id=1, username="testuser", first_name="TestName", last_name="LastTestName", hashed_password="test123")


# Override the default get_current_user dependency for testing
app.dependency_overrides[get_current_user] = override_get_current_user

# Create a TestClient to send requests to the FastAPI
client = TestClient(app)


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
