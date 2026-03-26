# Limelight v2 – Development Overview

## Project Structure
- `backend/` – FastAPI backend (modules, core, tests)
- `frontend-store/` – React store frontend
- `frontend-admin/` – React admin frontend (to be created)
- `docker-compose.yml` – Database container

## Completed Milestones
- [x] Backend foundation: FastAPI, SQLModel, Alembic, PostgreSQL via Docker
- [x] Minimal items API (test endpoint)
- [x] React store frontend with API client
- [x] Auth module: Google OAuth, session management, user/session models
- [x] Database migrations for users, sessions, items
- [x] Auth tests (6 tests, all passing)

## Current Focus
- [ ] Replace frontend mock auth with real /auth/me and /auth/logout calls
- [ ] Build products module (models, schemas, router, services, tests)
- [ ] Add image upload (compression on client, cloud storage)
- [ ] Build cart module
- [ ] Build orders module
- [ ] Admin endpoints with role checks
- [ ] Comprehensive tests for each module
- [ ] Deployment (Vercel + Render + Cloudinary)

## Module Notes
Each module (auth, products, cart, orders) will have its own:
- `models.py`
- `schemas.py`
- `services.py`
- `router.py`
- `tests/` folder with unit tests
- `issues.md` inside the module folder for specific todos.

## Running Tests
```bash
cd backend
python -m pytest