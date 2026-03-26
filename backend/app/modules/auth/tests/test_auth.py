import pytest
from datetime import datetime, timezone
from sqlmodel import create_engine, Session, SQLModel
from app.modules.auth.models import User, Session as AuthSession
from app.modules.auth.services import create_user, get_user_by_oauth, create_session, get_user_by_session_id, delete_session
from app.modules.auth.schemas import UserCreate, UserUpdate
from pydantic import ValidationError

@pytest.fixture
def engine():
    # Use a fresh in‑memory database for each test
    engine = create_engine("sqlite:///:memory:", connect_args={"check_same_thread": False})
    SQLModel.metadata.create_all(engine)
    yield engine
    engine.dispose()

@pytest.fixture
def db(engine):
    with Session(engine) as session:
        yield session

def test_create_user_default_role(db):
    user_data = UserCreate(
        email="test@example.com",
        name="Test User",
        oauth_provider="google",
        oauth_id="123456"
    )
    user = create_user(db, user_data)
    assert user.role == "customer"

def test_update_user_role(db):
    # Create user
    user_data = UserCreate(
        email="test2@example.com",
        name="Test User 2",
        oauth_provider="google",
        oauth_id="78910"
    )
    user = create_user(db, user_data)
    assert user.role == "customer"

    # Update role
    update_data = UserUpdate(role="admin")
    user.role = update_data.role
    db.add(user)
    db.commit()
    db.refresh(user)
    assert user.role == "admin"

def test_update_user_role_invalid():
    # Test that invalid role raises validation error
    with pytest.raises(ValidationError) as exc_info:
        UserUpdate(role="superuser")
    assert "Role must be \"customer\" or \"admin\"" in str(exc_info.value)

def test_create_and_validate_session(db):
    user_data = UserCreate(
        email="test3@example.com",
        name="Test User 3",
        oauth_provider="google",
        oauth_id="111"
    )
    user = create_user(db, user_data)
    db_session = create_session(db, user.id)
    assert db_session.session_id is not None
    assert db_session.user_id == user.id
    # Check expires_at is in future (allow small tolerance for test execution)
    now_naive = datetime.now(timezone.utc).replace(tzinfo=None)
    assert db_session.expires_at > now_naive

def test_get_user_by_session_id(db):
    user_data = UserCreate(
        email="test4@example.com",
        name="Test User 4",
        oauth_provider="google",
        oauth_id="222"
    )
    user = create_user(db, user_data)
    db_session = create_session(db, user.id)
    retrieved_user = get_user_by_session_id(db, db_session.session_id)
    assert retrieved_user is not None
    assert retrieved_user.id == user.id

def test_delete_session(db):
    user_data = UserCreate(
        email="test5@example.com",
        name="Test User 5",
        oauth_provider="google",
        oauth_id="333"
    )
    user = create_user(db, user_data)
    db_session = create_session(db, user.id)
    delete_session(db, db_session.session_id)
    # Verify it's gone
    retrieved = db.get(AuthSession, db_session.id)
    assert retrieved is None