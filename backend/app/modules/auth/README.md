# Auth Module

Handles user authentication and session management for Limelight.

## Overview

Provides Google OAuth login, session‑based authentication (HttpOnly cookies), and user role management. All protected endpoints rely on the `get_current_user` dependency.

## Environment Variables

The module requires the following variables in `.env`:

- `GOOGLE_CLIENT_ID`: OAuth client ID from Google Cloud Console
- `GOOGLE_CLIENT_SECRET`: OAuth client secret
- `SECRET_KEY`: used to sign session cookies (generate with `openssl rand -hex 32`)
- `OAUTH_REDIRECT_URI`: optional, defaults to `http://localhost:8000/auth/callback`

## Data Models

### `User` (SQLModel table)

| Field            | Type       | Description                               |
|------------------|------------|-------------------------------------------|
| `id`             | `int`      | Primary key                               |
| `email`          | `str`      | Unique, indexed                           |
| `name`           | `str?`     | Optional display name                     |
| `role`           | `str`      | `"customer"` or `"admin"` (default `"customer"`) |
| `oauth_provider` | `str?`     | e.g., `"google"`                          |
| `oauth_id`       | `str?`     | Unique ID from OAuth provider             |
| `created_at`     | `datetime` | Creation timestamp                        |
| `updated_at`     | `datetime` | Auto‑updated on change                    |

### `Session` (SQLModel table)

| Field         | Type       | Description                          |
|---------------|------------|--------------------------------------|
| `id`          | `int`      | Primary key                          |
| `session_id`  | `str`      | Random token, unique, indexed        |
| `user_id`     | `int`      | Foreign key to `users.id`            |
| `expires_at`  | `datetime` | Session expiration (default 7 days)  |
| `created_at`  | `datetime` | Creation timestamp                   |

## Schemas (Pydantic)

- `UserCreate`: used for creating a user via OAuth (email, name, oauth_provider, oauth_id)
- `UserRead`: full user data for responses (id, email, name, role, created_at, updated_at)
- `UserUpdate`: partial update (name, role) – role validated against `"customer"`/`"admin"`
- `SessionRead`: session data (session_id, expires_at)

## Services

Located in `services.py`:

- `create_user`: creates a user from OAuth data
- `get_user_by_oauth`: retrieves user by provider and oauth_id
- `create_session`: creates a session and returns session object
- `get_user_by_session_id`: validates session and returns associated user
- `delete_session`: removes a session (logout)
- `update_user`: updates user fields (name, role) – role validation performed

## API Endpoints

All endpoints are prefixed with `/auth`.

| Method | Endpoint | Description | Auth |
|--------|----------|-------------|------|
| GET | `/login` | Redirect to Google OAuth | none |
| GET | `/callback` | OAuth callback, creates user & session, sets cookie | none |
| POST | `/logout` | Clears session cookie and deletes session from DB | (cookie required) |
| GET | `/me` | Returns current user (requires session cookie) | session |

## Dependencies

- `get_current_user` (in `core/dependencies.py`) – validates session cookie and returns user
- `require_admin` – wrapper that checks `user.role == "admin"` (returns 403 otherwise)

## Testing

Run the module tests:

```bash
cd backend
python -m pytest app/modules/auth/tests/test_auth.py -v
```

## Tests cover:

    User creation with default role

    User update (role change)

    Session creation and validation

    Session deletion

    Schema validation for roles

    All service functions (using in‑memory SQLite)

## Notes

    Sessions are stored in the database and expire after 7 days.

    The session cookie is HttpOnly, SameSite=Lax, and not Secure in development (set Secure=True in production).

    OAuth is currently implemented only for Google; other providers can be added by registering them in router.py.

    The UserUpdate schema includes a role validator that only allows "customer" or "admin".