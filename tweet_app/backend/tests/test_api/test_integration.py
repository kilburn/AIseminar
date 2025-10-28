import pytest
import json
from httpx import AsyncClient
from fastapi import status


@pytest.mark.asyncio
class TestAuthenticationAPI:
    """Test Phase 1 authentication endpoints."""

    async def test_user_registration(self, client: AsyncClient, sample_user_data):
        """Test user registration endpoint."""
        response = await client.post(
            "/api/v1/auth/register",
            json={
                "username": sample_user_data["username"],
                "email": sample_user_data["email"],
                "password": sample_user_data["password"],
                "full_name": sample_user_data["full_name"]
            }
        )

        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        assert data["username"] == sample_user_data["username"]
        assert data["email"] == sample_user_data["email"]
        assert "id" in data
        assert "password" not in data  # Password should never be returned

    async def test_user_registration_duplicate_email(self, client: AsyncClient, sample_user_data):
        """Test registration fails with duplicate email."""
        # First registration
        await client.post(
            "/api/v1/auth/register",
            json={
                "username": sample_user_data["username"],
                "email": sample_user_data["email"],
                "password": sample_user_data["password"],
                "full_name": sample_user_data["full_name"]
            }
        )

        # Second registration with same email
        response = await client.post(
            "/api/v1/auth/register",
            json={
                "username": "different_user",
                "email": sample_user_data["email"],
                "password": sample_user_data["password"],
                "full_name": "Different User"
            }
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    async def test_user_login(self, client: AsyncClient, sample_user_data):
        """Test user login endpoint."""
        # Register user first
        await client.post(
            "/api/v1/auth/register",
            json={
                "username": sample_user_data["username"],
                "email": sample_user_data["email"],
                "password": sample_user_data["password"],
                "full_name": sample_user_data["full_name"]
            }
        )

        # Login
        response = await client.post(
            "/api/v1/auth/login",
            json={
                "email": sample_user_data["email"],
                "password": sample_user_data["password"]
            }
        )

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert "access_token" in data
        assert "token_type" in data
        assert data["token_type"] == "bearer"

    async def test_user_login_invalid_credentials(self, client: AsyncClient, sample_user_data):
        """Test login fails with invalid credentials."""
        # Register user
        await client.post(
            "/api/v1/auth/register",
            json={
                "username": sample_user_data["username"],
                "email": sample_user_data["email"],
                "password": sample_user_data["password"],
                "full_name": sample_user_data["full_name"]
            }
        )

        # Login with wrong password
        response = await client.post(
            "/api/v1/auth/login",
            json={
                "email": sample_user_data["email"],
                "password": "wrong_password"
            }
        )

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    async def test_protected_route_without_token(self, client: AsyncClient):
        """Test accessing protected route without token returns 401."""
        response = await client.get("/api/v1/datasets")
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    async def test_protected_route_with_valid_token(self, client: AsyncClient, sample_user_data):
        """Test accessing protected route with valid token."""
        # Register and login
        await client.post(
            "/api/v1/auth/register",
            json={
                "username": sample_user_data["username"],
                "email": sample_user_data["email"],
                "password": sample_user_data["password"],
                "full_name": sample_user_data["full_name"]
            }
        )

        login_response = await client.post(
            "/api/v1/auth/login",
            json={
                "email": sample_user_data["email"],
                "password": sample_user_data["password"]
            }
        )

        token = login_response.json()["access_token"]

        # Access protected route
        response = await client.get(
            "/api/v1/datasets",
            headers={"Authorization": f"Bearer {token}"}
        )

        assert response.status_code == status.HTTP_200_OK


@pytest.mark.asyncio
class TestDatasetManagementAPI:
    """Test Phase 1 dataset management endpoints."""

    async def _get_auth_token(self, client: AsyncClient, sample_user_data):
        """Helper to get authentication token."""
        await client.post(
            "/api/v1/auth/register",
            json={
                "username": sample_user_data["username"],
                "email": sample_user_data["email"],
                "password": sample_user_data["password"],
                "full_name": sample_user_data["full_name"]
            }
        )

        response = await client.post(
            "/api/v1/auth/login",
            json={
                "email": sample_user_data["email"],
                "password": sample_user_data["password"]
            }
        )

        return response.json()["access_token"]

    async def test_list_datasets(self, client: AsyncClient, sample_user_data):
        """Test listing datasets returns empty list initially."""
        token = await self._get_auth_token(client, sample_user_data)

        response = await client.get(
            "/api/v1/datasets",
            headers={"Authorization": f"Bearer {token}"}
        )

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert isinstance(data, list)
        assert len(data) == 0

    async def test_create_dataset(self, client: AsyncClient, sample_user_data, sample_dataset_data):
        """Test creating a dataset."""
        token = await self._get_auth_token(client, sample_user_data)

        response = await client.post(
            "/api/v1/datasets",
            headers={"Authorization": f"Bearer {token}"},
            json={
                "name": sample_dataset_data["name"],
                "description": sample_dataset_data["description"],
                "is_public": sample_dataset_data["is_public"]
            }
        )

        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        assert data["name"] == sample_dataset_data["name"]
        assert data["description"] == sample_dataset_data["description"]
        assert data["is_public"] == sample_dataset_data["is_public"]
        assert "id" in data
        assert "status" in data

    async def test_get_dataset_detail(self, client: AsyncClient, sample_user_data, sample_dataset_data):
        """Test getting dataset details."""
        token = await self._get_auth_token(client, sample_user_data)

        # Create dataset
        create_response = await client.post(
            "/api/v1/datasets",
            headers={"Authorization": f"Bearer {token}"},
            json={
                "name": sample_dataset_data["name"],
                "description": sample_dataset_data["description"]
            }
        )

        dataset_id = create_response.json()["id"]

        # Get dataset details
        response = await client.get(
            f"/api/v1/datasets/{dataset_id}",
            headers={"Authorization": f"Bearer {token}"}
        )

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["id"] == dataset_id
        assert data["name"] == sample_dataset_data["name"]

    async def test_update_dataset(self, client: AsyncClient, sample_user_data, sample_dataset_data):
        """Test updating dataset metadata."""
        token = await self._get_auth_token(client, sample_user_data)

        # Create dataset
        create_response = await client.post(
            "/api/v1/datasets",
            headers={"Authorization": f"Bearer {token}"},
            json={
                "name": sample_dataset_data["name"],
                "description": sample_dataset_data["description"]
            }
        )

        dataset_id = create_response.json()["id"]

        # Update dataset
        updated_name = "Updated Dataset Name"
        response = await client.put(
            f"/api/v1/datasets/{dataset_id}",
            headers={"Authorization": f"Bearer {token}"},
            json={
                "name": updated_name,
                "description": "Updated description"
            }
        )

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["name"] == updated_name

    async def test_delete_dataset(self, client: AsyncClient, sample_user_data, sample_dataset_data):
        """Test deleting a dataset."""
        token = await self._get_auth_token(client, sample_user_data)

        # Create dataset
        create_response = await client.post(
            "/api/v1/datasets",
            headers={"Authorization": f"Bearer {token}"},
            json={
                "name": sample_dataset_data["name"],
                "description": sample_dataset_data["description"]
            }
        )

        dataset_id = create_response.json()["id"]

        # Delete dataset
        response = await client.delete(
            f"/api/v1/datasets/{dataset_id}",
            headers={"Authorization": f"Bearer {token}"}
        )

        assert response.status_code == status.HTTP_204_NO_CONTENT

        # Verify deletion
        verify_response = await client.get(
            f"/api/v1/datasets/{dataset_id}",
            headers={"Authorization": f"Bearer {token}"}
        )

        assert verify_response.status_code == status.HTTP_404_NOT_FOUND

    async def test_unauthorized_dataset_access(self, client: AsyncClient, sample_user_data, sample_dataset_data):
        """Test user cannot access other user's private dataset."""
        # Create first user and dataset
        token1 = await self._get_auth_token(client, sample_user_data)

        create_response = await client.post(
            "/api/v1/datasets",
            headers={"Authorization": f"Bearer {token1}"},
            json={
                "name": sample_dataset_data["name"],
                "description": sample_dataset_data["description"],
                "is_public": False
            }
        )

        dataset_id = create_response.json()["id"]

        # Create second user
        second_user_data = {
            "username": "seconduser",
            "email": "second@example.com",
            "password": "password123",
            "full_name": "Second User"
        }

        token2 = await self._get_auth_token(client, second_user_data)

        # Try to access first user's private dataset
        response = await client.get(
            f"/api/v1/datasets/{dataset_id}",
            headers={"Authorization": f"Bearer {token2}"}
        )

        assert response.status_code == status.HTTP_403_FORBIDDEN
