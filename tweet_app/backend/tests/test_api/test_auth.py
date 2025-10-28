import pytest
from httpx import AsyncClient
from app.core.security import create_access_token, verify_password, get_password_hash


class TestAuthAPI:
    """Test authentication API endpoints."""

    async def test_register_user(self, client: AsyncClient, sample_user_data):
        """Test user registration."""
        response = await client.post("/api/v1/auth/register", json=sample_user_data)
        assert response.status_code == 201

        data = response.json()
        assert data["username"] == sample_user_data["username"]
        assert data["email"] == sample_user_data["email"]
        assert data["full_name"] == sample_user_data["full_name"]
        assert data["organization"] == sample_user_data["organization"]
        assert "id" in data
        assert "password" not in data

    async def test_register_user_duplicate_email(self, client: AsyncClient, sample_user_data):
        """Test registration with duplicate email fails."""
        # First registration
        await client.post("/api/v1/auth/register", json=sample_user_data)

        # Second registration with same email
        response = await client.post("/api/v1/auth/register", json=sample_user_data)
        assert response.status_code == 400
        assert "already registered" in response.json()["detail"].lower()

    async def test_login_success(self, client: AsyncClient, sample_user_data):
        """Test successful login."""
        # Register user first
        await client.post("/api/v1/auth/register", json=sample_user_data)

        # Login
        login_data = {
            "username": sample_user_data["email"],
            "password": sample_user_data["password"]
        }
        response = await client.post("/api/v1/auth/login", data=login_data)
        assert response.status_code == 200

        data = response.json()
        assert "access_token" in data
        assert "refresh_token" in data
        assert data["token_type"] == "bearer"

    async def test_login_invalid_credentials(self, client: AsyncClient, sample_user_data):
        """Test login with invalid credentials."""
        # Register user first
        await client.post("/api/v1/auth/register", json=sample_user_data)

        # Login with wrong password
        login_data = {
            "username": sample_user_data["email"],
            "password": "wrongpassword"
        }
        response = await client.post("/api/v1/auth/login", data=login_data)
        assert response.status_code == 401
        assert "incorrect" in response.json()["detail"].lower()

    async def test_login_nonexistent_user(self, client: AsyncClient):
        """Test login with nonexistent user."""
        login_data = {
            "username": "nonexistent@example.com",
            "password": "password123"
        }
        response = await client.post("/api/v1/auth/login", data=login_data)
        assert response.status_code == 401
        assert "incorrect" in response.json()["detail"].lower()

    async def test_get_current_user(self, client: AsyncClient, sample_user_data):
        """Test getting current user info."""
        # Register and login
        await client.post("/api/v1/auth/register", json=sample_user_data)

        login_data = {
            "username": sample_user_data["email"],
            "password": sample_user_data["password"]
        }
        login_response = await client.post("/api/v1/auth/login", data=login_data)
        token = login_response.json()["access_token"]

        # Get current user
        headers = {"Authorization": f"Bearer {token}"}
        response = await client.get("/api/v1/auth/me", headers=headers)
        assert response.status_code == 200

        data = response.json()
        assert data["username"] == sample_user_data["username"]
        assert data["email"] == sample_user_data["email"]

    async def test_get_current_user_invalid_token(self, client: AsyncClient):
        """Test getting current user with invalid token."""
        headers = {"Authorization": "Bearer invalid_token"}
        response = await client.get("/api/v1/auth/me", headers=headers)
        assert response.status_code == 401

    async def test_get_current_user_no_token(self, client: AsyncClient):
        """Test getting current user without token."""
        response = await client.get("/api/v1/auth/me")
        assert response.status_code == 401


class TestAuthSecurity:
    """Test authentication security utilities."""

    def test_password_hashing(self):
        """Test password hashing and verification."""
        password = "test_password_123"
        hashed = get_password_hash(password)

        assert hashed != password
        assert verify_password(password, hashed)
        assert not verify_password("wrong_password", hashed)

    def test_create_access_token(self):
        """Test JWT token creation."""
        data = {"sub": "test@example.com"}
        token = create_access_token(data)

        assert isinstance(token, str)
        assert len(token) > 0

    def test_create_access_token_with_expiry(self):
        """Test JWT token creation with custom expiry."""
        data = {"sub": "test@example.com"}
        token = create_access_token(data, expires_delta=60)

        assert isinstance(token, str)
        assert len(token) > 0