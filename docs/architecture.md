# Limelight v2 – Architecture Overview

## Tech Stack

- **Backend**: FastAPI (Python 3.12), SQLModel (ORM), PostgreSQL
- **Migrations**: Alembic
- **Auth**: Google OAuth, session cookies (HttpOnly)
- **Testing**: pytest (module‑level tests with in‑memory SQLite)
- **Deployment**: Render (backend), Vercel (frontend – planned)
- **Container**: Docker (development)

## Modular Structure

backend/app/modules/

├── auth/      # user, session, OAuth

├── products/  # product CRUD, soft delete

├── cart/     # cart items, stock validation

└── orders/         |# order creation from cart, status transitions

Each module has:

- `models.py` – SQLModel tables
- `schemas.py` – Pydantic request/response
- `services.py` – business logic
- `router.py` – FastAPI endpoints
- `tests/` – unit tests (pytest)

## Key Design Decisions

- **No cross‑module relationships** in models – foreign keys only. Enrichment happens in routers via explicit joins. This avoids circular imports.
- **Soft delete** for products (`deleted_at` timestamp). Public endpoints exclude deleted items.
- **Session‑based auth** (not JWT) – simpler for MVP, secure with HttpOnly cookies.
- **Role‑based access** – `customer` (default), `admin`. Future: `seller`.
- **Cart & order stock validation** – done in transactions.

## Testing

Run all module tests from `backend/`:

```bash
pytest app/modules/ -v
```

## Environment Variables

See backend/.env.example (create your own .env). Required:
    **DATABASE_URL**
    **GOOGLE_CLIENT_ID**, **GOOGLE_CLIENT_SECRET**
    **SECRET_KEY**
    **OAUTH_REDIRECT_URI**

## Deployment

- Backend: Render (see docker-compose.yml for local DB)
- Database: Render PostgreSQL (internal connection)
