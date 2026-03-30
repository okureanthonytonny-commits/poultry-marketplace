from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import items  # your existing items router
from app.modules.auth.router import router as auth_router
from app.modules.products.router import router as products_router
from app.core.config import settings
from starlette.middleware.sessions import SessionMiddleware

app = FastAPI(title="Limelight v2")

app.add_middleware(
    SessionMiddleware,
    secret_key=settings.SECRET_KEY,
    session_cookie="session_id",
    max_age=7 * 24 * 60 * 60,
    same_site="lax",
    https_only=False,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(items.router, prefix="/api/items")
app.include_router(auth_router, prefix="/api/auth")
app.include_router(products_router, prefix="/api")

@app.get("/")
def root():
    return {"message": "Limelight v2 API"}
