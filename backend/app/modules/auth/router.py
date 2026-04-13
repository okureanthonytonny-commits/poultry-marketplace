import secrets
from datetime import datetime, timedelta
from fastapi import APIRouter, Depends, HTTPException, Request, Response
from sqlmodel import Session as DBSession
from starlette.responses import RedirectResponse
from authlib.integrations.starlette_client import OAuth
from starlette.config import Config
from app.core.database import get_session
from app.core.config import settings
from app.core.dependencies import require_admin
from app.modules.auth.models import User
from .services import create_user, get_user_by_oauth, create_session, get_user_by_session_id, delete_session, update_user, update_user
from .schemas import UserCreate, UserRead, UserUpdate

router = APIRouter(prefix="/auth", tags=["auth"])

oauth = OAuth()
oauth.register(
    name='google',
    client_id=settings.GOOGLE_CLIENT_ID,
    client_secret=settings.GOOGLE_CLIENT_SECRET,
    server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
    client_kwargs={'scope': 'openid email profile'},
)

@router.patch("/admin/users/{user_id}", response_model=UserRead)
def admin_update_user(
    user_id: int,
    update_data: UserUpdate,
    db: DBSession = Depends(get_session),
    _: User = Depends(require_admin)
):
    user = update_user(db, user_id, update_data)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.get("/login")
async def login(request: Request):
    """Redirect to Google OAuth login"""
    redirect_uri = settings.OAUTH_REDIRECT_URI
    return await oauth.google.authorize_redirect(request, redirect_uri)

@router.get("/callback")
async def callback(request: Request, db: DBSession = Depends(get_session)):
    """Handle OAuth callback"""
    try:
        token = await oauth.google.authorize_access_token(request)
        userinfo = token.get('userinfo')
        if not userinfo:
            userinfo = await oauth.google.parse_id_token(request, token)
        email = userinfo.get('email')
        name = userinfo.get('name')
        google_id = userinfo.get('sub')
        if not email or not google_id:
            raise HTTPException(400, "Incomplete user info")

        # Check if user exists
        user = get_user_by_oauth(db, "google", google_id)
        if not user:
            user = create_user(db, UserCreate(
                email=email,
                name=name,
                oauth_provider="google",
                oauth_id=google_id,
            ))
        # Create session
        db_session = create_session(db, user.id)
        response = RedirectResponse(url="/")
        response.set_cookie(
            key="session_id",
            value=db_session.session_id,
            httponly=True,
            secure=False,   # set True in production
            samesite="lax",
            max_age=7*24*60*60,
        )
        return response
    except Exception as e:
        raise HTTPException(400, detail=str(e))

@router.post("/logout")
async def logout(request: Request, response: Response, db: DBSession = Depends(get_session)):
    session_id = request.cookies.get("session_id")
    if session_id:
        delete_session(db, session_id)
    response.delete_cookie("session_id")
    return {"message": "Logged out"}

@router.get("/me", response_model=UserRead)
async def get_me(request: Request, db: DBSession = Depends(get_session)):
    session_id = request.cookies.get("session_id")
    if not session_id:
        raise HTTPException(401, "Not authenticated")
    user = get_user_by_session_id(db, session_id)
    if not user:
        raise HTTPException(401, "Invalid or expired session")
    return user