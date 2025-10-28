import pytest
import uuid
from httpx import AsyncClient
from app.models.user import User
from app.models.dataset import Dataset
from app.core.security import get_password_hash


class TestDatasetsAPI:
    """Test dataset management API endpoints."""

    async def create_test_user(self, client: AsyncClient, sample_user_data):
        """Helper to create a test user and return auth token."""
        await client.post("/api/v1/auth/register", json=sample_user_data)

        login_data = {
            "username": sample_user_data["email"],
            "password": sample_user_data["password"]
        }
        login_response = await client.post("/api/v1/auth/login", data=login_data)
        return login_response.json()["access_token"]

    async def test_create_dataset(self, client: AsyncClient, sample_user_data, sample_dataset_data):
        """Test dataset creation."""
        token = await self.create_test_user(client, sample_user_data)
        headers = {"Authorization": f"Bearer {token}"}

        response = await client.post("/api/v1/datasets/", json=sample_dataset_data, headers=headers)
        assert response.status_code == 201

        data = response.json()
        assert data["name"] == sample_dataset_data["name"]
        assert data["description"] == sample_dataset_data["description"]
        assert data["is_public"] == sample_dataset_data["is_public"]
        assert "id" in data
        assert data["processing_status"] == "pending"

    async def test_create_dataset_unauthorized(self, client: AsyncClient, sample_dataset_data):
        """Test dataset creation without authentication."""
        response = await client.post("/api/v1/datasets/", json=sample_dataset_data)
        assert response.status_code == 401

    async def test_list_datasets_empty(self, client: AsyncClient, sample_user_data):
        """Test listing datasets when user has none."""
        token = await self.create_test_user(client, sample_user_data)
        headers = {"Authorization": f"Bearer {token}"}

        response = await client.get("/api/v1/datasets/", headers=headers)
        assert response.status_code == 200
        assert response.json() == []

    async def test_list_datasets_with_data(self, client: AsyncClient, sample_user_data, sample_dataset_data):
        """Test listing datasets when user has some."""
        token = await self.create_test_user(client, sample_user_data)
        headers = {"Authorization": f"Bearer {token}"}

        # Create two datasets
        await client.post("/api/v1/datasets/", json=sample_dataset_data, headers=headers)

        dataset2_data = sample_dataset_data.copy()
        dataset2_data["name"] = "Second Dataset"
        await client.post("/api/v1/datasets/", json=dataset2_data, headers=headers)

        response = await client.get("/api/v1/datasets/", headers=headers)
        assert response.status_code == 200
        datasets = response.json()
        assert len(datasets) == 2

    async def test_get_dataset_by_id(self, client: AsyncClient, sample_user_data, sample_dataset_data):
        """Test getting a specific dataset."""
        token = await self.create_test_user(client, sample_user_data)
        headers = {"Authorization": f"Bearer {token}"}

        # Create dataset
        create_response = await client.post("/api/v1/datasets/", json=sample_dataset_data, headers=headers)
        dataset_id = create_response.json()["id"]

        # Get dataset
        response = await client.get(f"/api/v1/datasets/{dataset_id}", headers=headers)
        assert response.status_code == 200

        data = response.json()
        assert data["id"] == dataset_id
        assert data["name"] == sample_dataset_data["name"]

    async def test_get_dataset_not_found(self, client: AsyncClient, sample_user_data):
        """Test getting a non-existent dataset."""
        token = await self.create_test_user(client, sample_user_data)
        headers = {"Authorization": f"Bearer {token}"}

        fake_id = uuid.uuid4()
        response = await client.get(f"/api/v1/datasets/{fake_id}", headers=headers)
        assert response.status_code == 404

    async def test_update_dataset(self, client: AsyncClient, sample_user_data, sample_dataset_data):
        """Test updating a dataset."""
        token = await self.create_test_user(client, sample_user_data)
        headers = {"Authorization": f"Bearer {token}"}

        # Create dataset
        create_response = await client.post("/api/v1/datasets/", json=sample_dataset_data, headers=headers)
        dataset_id = create_response.json()["id"]

        # Update dataset
        update_data = {
            "name": "Updated Dataset Name",
            "description": "Updated description",
            "is_public": True
        }
        response = await client.put(f"/api/v1/datasets/{dataset_id}", json=update_data, headers=headers)
        assert response.status_code == 200

        data = response.json()
        assert data["name"] == update_data["name"]
        assert data["description"] == update_data["description"]
        assert data["is_public"] == update_data["is_public"]

    async def test_delete_dataset(self, client: AsyncClient, sample_user_data, sample_dataset_data):
        """Test deleting a dataset."""
        token = await self.create_test_user(client, sample_user_data)
        headers = {"Authorization": f"Bearer {token}"}

        # Create dataset
        create_response = await client.post("/api/v1/datasets/", json=sample_dataset_data, headers=headers)
        dataset_id = create_response.json()["id"]

        # Delete dataset
        response = await client.delete(f"/api/v1/datasets/{dataset_id}", headers=headers)
        assert response.status_code == 204

        # Verify deletion
        get_response = await client.get(f"/api/v1/datasets/{dataset_id}", headers=headers)
        assert get_response.status_code == 404

    async def test_dataset_validation(self, client: AsyncClient, sample_user_data):
        """Test dataset creation validation."""
        token = await self.create_test_user(client, sample_user_data)
        headers = {"Authorization": f"Bearer {token}"}

        # Test empty name
        invalid_data = {"name": "", "description": "Test"}
        response = await client.post("/api/v1/datasets/", json=invalid_data, headers=headers)
        assert response.status_code == 422

        # Test name too long
        invalid_data = {"name": "a" * 256, "description": "Test"}
        response = await client.post("/api/v1/datasets/", json=invalid_data, headers=headers)
        assert response.status_code == 422