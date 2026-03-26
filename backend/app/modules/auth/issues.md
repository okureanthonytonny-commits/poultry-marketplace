# Auth Module – Issues & Notes

## Completed
- [x] User and Session models
- [x] OAuth integration with Google
- [x] Session cookie management
- [x] Authentication endpoints (/login, /callback, /logout)
- [x] Dependencies: get_current_user, require_admin
- [x] Pydantic schemas for request/response
- [x] User update service (for role changes)
- [x] Alembic migrations for users and sessions
- [x] Unit tests for services and schemas
- [x] Updated_at auto‑update using SQLAlchemy onupdate

## Remaining / Future Enhancements
- [ ] Admin endpoint to promote users to admin (currently manual DB update)
- [ ] Password-based authentication (if needed later)
- [ ] Rate limiting on login attempts
- [ ] Email verification flow
- [ ] Integration with frontend (currently mock in frontend-store)
- [ ] More comprehensive tests for OAuth edge cases