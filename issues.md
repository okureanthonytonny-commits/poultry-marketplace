# Limelight v2 – Development Issues

## Completed

- [x] Project setup with Docker, FastAPI, SQLModel, Alembic
- [x] Minimal items API (test endpoint)
- [x] React frontend with API client
- [x] Auth module: Google OAuth, session cookies, user/session models
- [x] Database migrations for users, sessions, items
- [x] Fix user role storage (store lowercase string)
- [x] Auto‑update `updated_at` on user updates
- [x] Tests for auth (6 tests passing)
- [x] Products module: CRUD, soft delete, duplicate name check, tests
- [x] Cart module: add, update, remove, clear, tests
- [x] Orders module: create from cart, list, detail, status update, enrichment, tests
- [x] Integration tests for authenticated endpoints (bash script)
- [X] Removed old traces of "item model". It was used to test functionality before the actual build started.
- [X] Removed fronte*/
- [X] Moving test scripts and docs to tests/ and docs/

## In Progress / Next

- [ ] Replace frontend mock auth with real `/auth/me` and `/auth/logout` calls
- [ ] Build admin frontend for product management
- [ ] Add image upload (compression on client, cloud storage)
- [ ] Deployment to production (Vercel + Render + Cloudinary)
- [ ] Write comprehensive documentation (API, setup, deployment)
