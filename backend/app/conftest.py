import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine, StaticPool
from app.main import app  # Assumes your FastAPI app is initialized here
from app.core.database import get_session
from app.modules.auth.models import User, Session as DBSession
from datetime import datetime, timedelta, timezone

# 1. Setup an in-memory SQLite database for fast, isolated tests
@pytest.fixture(name="session")
def session_fixture():
    engine = create_engine(
        "sqlite://", 
        connect_args={"check_same_thread": False}, 
        poolclass=StaticPool
    )
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session

# 2. Override the production database dependency with the test session
@pytest.fixture(name="client")
def client_fixture(session: Session):
    def get_session_override():
        return session
    app.dependency_overrides[get_session] = get_session_override
    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()

# 3. Helper fixture to create a test user
@pytest.fixture
def test_user(session: Session):
    user = User(
        email="test@example.com",
        name="Test User",
        role="customer",
        oauth_provider="google",
        oauth_id="12345"
    )
    session.add(user)
    session.commit()
    session.refresh(user)
    return user

# 4. Helper fixture to simulate an authenticated session
@pytest.fixture
def auth_client(client, test_user, session: Session):
    db_session = DBSession(
        session_id="test-token-abc",
        user_id=test_user.id,
        expires_at=datetime.now(timezone.utc) + timedelta(days=1)
    )
    session.add(db_session)
    session.commit()
    client.cookies.set("session_id", db_session.session_id)
    return client

@pytest.fixture
def admin_user(session: Session):
    user = User(
        email="okureanthonytonny@gmail.com",
        name="Admin User",
        role="admin",
        oauth_provider="google",
        oauth_id="admin_123"
    )
    session.add(user)
    session.commit()
    session.refresh(user)
    return user

@pytest.fixture
def admin_client(client, admin_user, session: Session):
    db_session = DBSession(
        session_id="admin-token-abc",
        user_id=admin_user.id,
        expires_at=datetime.now(timezone.utc) + timedelta(days=1)
    )
    session.add(db_session)
    session.commit()
    client.cookies.set("session_id", db_session.session_id)
    return client