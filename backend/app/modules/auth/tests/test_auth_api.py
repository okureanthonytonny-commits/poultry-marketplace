import pytest
from app.modules.auth.models import User

def test_get_me_unauthenticated(client):
    """Verify that /auth/me returns 401 for anonymous users."""
    response = client.get("/auth/me")
    assert response.status_code == 401

def test_get_me_authenticated(auth_client, test_user):
    """Verify that /auth/me identifies the correct user."""
    response = auth_client.get("/auth/me")
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == test_user.email
    assert data["role"] == "customer"

def test_admin_promote_and_demote_user(admin_client, test_user):
    """Verify that an admin can promote and demote a user."""
    # Promote
    response = admin_client.patch(f"/auth/admin/users/{test_user.id}", json={"role": "admin"})
    assert response.status_code == 200
    assert response.json()["role"] == "admin"

    # Demote
    response = admin_client.patch(f"/auth/admin/users/{test_user.id}", json={"role": "customer"})
    assert response.status_code == 200
    assert response.json()["role"] == "customer"

def test_customer_self_promotion_forbidden(auth_client, test_user):
    """Verify that a customer cannot change their own role via PATCH /auth/me."""
    response = auth_client.patch("/auth/me", json={"role": "admin"})
    # Check that the role remains 'customer' or endpoint is restricted
    if response.status_code == 200:
        assert response.json()["role"] == "customer"
    else:
        assert response.status_code in (403, 404, 405)