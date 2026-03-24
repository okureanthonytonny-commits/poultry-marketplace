# Limelight v2 – Development Issues

## Completed
- [x] Project setup with Docker, FastAPI, SQLModel, Alembic
- [x] Minimal items API (test endpoint)
- [x] React frontend with API client
- [x] Auth module: Google OAuth, session cookies, user/session models
- [x] Database migrations for users, sessions, items

## In Progress / Next
- [ ] Fix user role storage: currently stores enum name, should store value (quick fix: use string with validation)
- [ ] Replace frontend mock auth with real /auth/me and /auth/logout calls
- [ ] Build products module (models, schemas, router, services, tests)
- [ ] Add image upload (compression on client, cloud storage)
- [ ] Build cart module
- [ ] Build orders module
- [ ] Add admin endpoints with role checks
- [ ] Write comprehensive tests for each module
- [ ] Deployment to production (Vercel + Render + Cloudinary)