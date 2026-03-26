
### Backend issues.md (backend/)

```markdown
# Backend Development – Issues & Notes

## Completed
- [x] Core configuration (config.py, database.py)
- [x] CORS and SessionMiddleware setup
- [x] Alembic migrations system
- [x] Items test endpoint (temporary)
- [x] Auth module (complete)

## Auth Module Details
- Models: User, Session
- OAuth: Google (authlib)
- Session cookies (HttpOnly)
- Dependencies: get_current_user, require_admin
- Services: create_user, get_user_by_oauth, create_session, get_user_by_session_id, delete_session, update_user
- Schemas: UserCreate, UserRead, UserUpdate, SessionRead
- Tests: 6 unit tests, all passing
- Migrations: all applied (users, sessions, items)

## Next Steps
- [ ] Products module:
  - Model: Product (id, name, description, price, stock, image_url, created_at, updated_at)
  - Public endpoints: GET /products, GET /products/{id}
  - Admin endpoints: POST /admin/products, PUT /admin/products/{id}, DELETE /admin/products/{id}
  - Image upload: handle via static files (development) and cloud storage (production)
  - Tests
- [ ] Cart module (depends on auth and products)
- [ ] Orders module (depends on cart and products)

## Testing
```bash
python -m pytest tests/      # integration tests
python -m pytest app/modules/auth/tests   # unit tests