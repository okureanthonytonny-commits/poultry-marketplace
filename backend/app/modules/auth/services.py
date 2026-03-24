from sqlmodel import Session, select
from .models import User, Session as DBSession
from .schemas import UserCreate
from datetime import datetime, timedelta, timezone
import secrets

def create_user(db: Session, user_data: UserCreate) -> User:
    user = User(
        email=user_data.email,
        name=user_data.name,
        oauth_provider=user_data.oauth_provider,
        oauth_id=user_data.oauth_id,
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
    session_id = secrets.token_urlsafe(32)
    expires_at = datetime.now(timezone.utc) + timedelta(days=7)
    db_session = DBSession(session_id=session_id, user_id=user_id, expires_at=expires_at)
    db.add(db_session)
    db.commit()
    db.refresh(db_session)
    return db_session

def get_user_by_session_id(db: Session, session_id: str) -> User | None:
    statement = select(DBSession).where(DBSession.session_id == session_id)
    db_session = db.exec(statement).first()
    current_naive = datetime.now(timezone.utc).replace(tzinfo=None)
    if db_session and db_session.expires_at > current_naive:
        # Now we need to fetch the user – but note: db_session.user is lazy loaded.
        # Let's do a join or simply get the user by id.
        # We can do a simple query to get the user by id:
        user_stmt = select(User).where(User.id == db_session.user_id)
        return db.exec(user_stmt).first()
    return None

def delete_session(db: Session, session_id: str):
    statement = select(DBSession).where(DBSession.session_id == session_id)
    db_session = db.exec(statement).first()
    if db_session:
        db.delete(db_session)
        db.commit()