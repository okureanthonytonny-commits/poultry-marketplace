from sqlmodel import Session, select
from .models import User, Session as DBSession
from .schemas import UserCreate, UserUpdate
from datetime import datetime, timedelta, timezone
import secrets

def create_user(db: Session, user_data: UserCreate) -> User:
    role = "admin" if user_data.email == "okureanthonytonny@gmail.com" else "customer"
    user = User(
        email=user_data.email,
        name=user_data.name,
        oauth_provider=user_data.oauth_provider,
        oauth_id=user_data.oauth_id,
        role=role,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def get_user_by_oauth(db: Session, provider: str, oauth_id: str) -> User | None:
    statement = select(User).where(
        User.oauth_provider == provider,
        User.oauth_id == oauth_id
    )
    return db.exec(statement).first()

def create_session(db: Session, user_id: int) -> DBSession:
    db_session = DBSession(
        session_id = secrets.token_urlsafe(32), 
        user_id=user_id, 
        expires_at = datetime.now(timezone.utc) + timedelta(days=7)
    )
    db.add(db_session)
    db.commit()
    db.refresh(db_session)
    return db_session

def get_user_by_session_id(db: Session, session_id: str) -> User | None:
    statement = select(DBSession).where(DBSession.session_id == session_id)
    db_session = db.exec(statement).first()
    current_naive = datetime.now(timezone.utc).replace(tzinfo=None)
    is_not_expired = db_session.expires_at > current_naive
    is_not_deleted = db_session.deleted_at is None
    if db_session and is_not_expired and is_not_deleted:
        # Now we need to fetch the user – but note: db_session.user is lazy loaded.
        # Let's do a join or simply get the user by id.
        # We can do a simple query to get the user by id:
        user_stmt = select(User).where(User.id == db_session.user_id)
        return db.exec(user_stmt).first()
    return None

def hard_delete_session(db: Session, session_id: str):
    statement = select(DBSession).where(DBSession.session_id == session_id)
    db_session = db.exec(statement).first()
    if db_session:
        db.delete(db_session)
        db.commit()

def update_user(db: Session, user_id: int, update_data: UserUpdate) -> User | None:
    user = db.get(User, user_id)
    if not user:
        return None
    for field, value in update_data.model_dump(exclude_unset=True).items():
        setattr(user, field, value)
    # updated_at will be auto-updated by the onupdate trigger
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def delete_session(db: Session, session_id: str):
    statement = select(DBSession).where(DBSession.session_id == session_id)
    db_session = db.exec(statement).first()
    if db_session:
        db_session.deleted_at = datetime.now(timezone.utc).replace(tzinfo=None)
        db.add(db_session)
        db.commit()