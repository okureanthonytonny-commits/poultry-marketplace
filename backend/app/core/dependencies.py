from fastapi import Depends, HTTPException, Request
from sqlmodel import Session
from app.core.database import get_session
from app.modules.auth.services import get_user_by_session_id
from app.modules.auth.models import User

def get_current_user(request: Request, db: Session = Depends(get_session)) -> User:
    session_id = request.cookies.get("session_id")
    if not session_id:
        raise HTTPException(401, "Not authenticated")
    user = get_user_by_session_id(db, session_id)
    if not user:
        raise HTTPException(401, "Invalid or expired session")
    return user

def require_admin(current_user: User = Depends(get_current_user)) -> User:
    if current_user.role != "admin":
        raise HTTPException(403, "Admin privileges required")
    return current_user
