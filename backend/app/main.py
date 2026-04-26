from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from app.modules.auth.router import router as auth_router
from app.modules.products.router import router as products_router
from app.modules.cart.router import router as cart_router
from app.modules.orders.router import router as orders_router
from app.core.config import settings
from app.core.errors import DomainError
from starlette.middleware.sessions import SessionMiddleware

app = FastAPI(title="Limelight v2")


@app.exception_handler(DomainError)
async def domain_error_handler(request: Request, exc: DomainError):
    return JSONResponse(status_code=exc.status_code, content={"detail": str(exc)})

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