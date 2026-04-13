from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.modules.auth.router import router as auth_router
from app.modules.products.router import router as products_router
from app.modules.cart.router import router as cart_router
from app.modules.orders.router import router as orders_router
from app.core.config import settings
from starlette.middleware.sessions import SessionMiddleware

app = FastAPI(title="Limelight v2")

app.add_middleware(
    SessionMiddleware,
    secret_key=settings.SECRET_KEY,
    session_cookie="session_state",
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


app.include_router(auth_router)
app.include_router(products_router)
app.include_router(cart_router)
app.include_router(orders_router)

@app.get("/")
def root():
    return {"message": "Limelight v2 API"}