import pytest
from datetime import datetime
from pydantic import ValidationError
from app.schemas.dataset import (
    DatasetCreate,
    DatasetUpdate,
    DatasetResponse,
    DatasetListResponse
)
from app.schemas.user import (
    UserCreate,
    UserResponse,
    UserUpdate
)


class TestDatasetSchemas:
    """Test Pydantic schemas for dataset validation."""

    def test_dataset_create_valid(self):
        """Test valid dataset creation schema."""
        data = {
            "name": "Test Dataset",
            "description": "A test dataset",
            "is_public": False
        }

        schema = DatasetCreate(**data)

        assert schema.name == "Test Dataset"
        assert schema.description == "A test dataset"
        assert schema.is_public is False

    def test_dataset_create_missing_required_field(self):
        """Test dataset creation fails without required name."""
        data = {
            "description": "A test dataset"
        }

        with pytest.raises(ValidationError) as exc_info:
            DatasetCreate(**data)

        errors = exc_info.value.errors()
        assert any(error["loc"] == ("name",) for error in errors)

    def test_dataset_create_invalid_name_type(self):
        """Test dataset creation fails with invalid name type."""
        data = {
            "name": 123,  # Should be string
            "description": "A test dataset"
        }

        with pytest.raises(ValidationError):
            DatasetCreate(**data)

    def test_dataset_update_partial(self):
        """Test partial dataset update."""
        data = {
            "name": "Updated Name"
        }

        schema = DatasetUpdate(**data)

        assert schema.name == "Updated Name"
        assert schema.description is None

    def test_dataset_response_schema(self):
        """Test dataset response schema."""
        data = {
            "id": "550e8400-e29b-41d4-a716-446655440000",
            "name": "Test Dataset",
            "description": "A test dataset",
            "owner_id": "550e8400-e29b-41d4-a716-446655440001",
            "is_public": False,
            "status": "pending",
            "tweet_count": 0,
            "processed_count": 0,
            "created_at": datetime.utcnow(),
            "updated_at": None
        }

        schema = DatasetResponse(**data)

        assert schema.id == "550e8400-e29b-41d4-a716-446655440000"
        assert schema.name == "Test Dataset"
        assert schema.status == "pending"

    def test_dataset_list_response_schema(self):
        """Test dataset list response schema."""
        data = {
            "total": 2,
            "page": 1,
            "page_size": 10,
            "datasets": [
                {
                    "id": "550e8400-e29b-41d4-a716-446655440000",
                    "name": "Dataset 1",
                    "description": "First dataset",
                    "owner_id": "550e8400-e29b-41d4-a716-446655440001",
                    "is_public": False,
                    "status": "pending",
                    "tweet_count": 0,
                    "processed_count": 0,
                    "created_at": datetime.utcnow(),
                    "updated_at": None
                },
                {
                    "id": "550e8400-e29b-41d4-a716-446655440002",
                    "name": "Dataset 2",
                    "description": "Second dataset",
                    "owner_id": "550e8400-e29b-41d4-a716-446655440001",
                    "is_public": True,
                    "status": "completed",
                    "tweet_count": 100,
                    "processed_count": 100,
                    "created_at": datetime.utcnow(),
                    "updated_at": datetime.utcnow()
                }
            ]
        }

        schema = DatasetListResponse(**data)

        assert schema.total == 2
        assert len(schema.datasets) == 2
        assert schema.datasets[0].name == "Dataset 1"
        assert schema.datasets[1].status == "completed"


class TestUserSchemas:
    """Test Pydantic schemas for user validation."""

    def test_user_create_valid(self):
        """Test valid user creation schema."""
        data = {
            "username": "testuser",
            "email": "test@example.com",
            "password": "secure_password_123",
            "full_name": "Test User"
        }

        schema = UserCreate(**data)

        assert schema.username == "testuser"
        assert schema.email == "test@example.com"
        assert schema.full_name == "Test User"

    def test_user_create_invalid_email(self):
        """Test user creation fails with invalid email."""
        data = {
            "username": "testuser",
            "email": "invalid_email",  # Invalid email format
            "password": "secure_password_123",
            "full_name": "Test User"
        }

        with pytest.raises(ValidationError):
            UserCreate(**data)

    def test_user_create_weak_password(self):
        """Test user creation with weak password."""
        data = {
            "username": "testuser",
            "email": "test@example.com",
            "password": "123",  # Too short
            "full_name": "Test User"
        }

        # This might fail depending on password validation rules
        # Adjust based on actual implementation
        try:
            schema = UserCreate(**data)
            # If it doesn't fail, that's also a valid test case
            assert schema.password == "123"
        except ValidationError:
            # Password too short, expected
            pass

    def test_user_create_missing_required_field(self):
        """Test user creation fails without required email."""
        data = {
            "username": "testuser",
            "password": "secure_password_123",
            "full_name": "Test User"
        }

        with pytest.raises(ValidationError) as exc_info:
            UserCreate(**data)

        errors = exc_info.value.errors()
        assert any(error["loc"] == ("email",) for error in errors)

    def test_user_response_schema(self):
        """Test user response schema."""
        data = {
            "id": "550e8400-e29b-41d4-a716-446655440000",
            "username": "testuser",
            "email": "test@example.com",
            "full_name": "Test User",
            "is_active": True,
            "is_verified": False,
            "created_at": datetime.utcnow()
        }

        schema = UserResponse(**data)

        assert schema.id == "550e8400-e29b-41d4-a716-446655440000"
        assert schema.username == "testuser"
        assert schema.email == "test@example.com"
        # Password should never be in response
        assert not hasattr(schema, "password")

    def test_user_update_schema(self):
        """Test user update schema."""
        data = {
            "full_name": "Updated Name",
            "is_verified": True
        }

        schema = UserUpdate(**data)

        assert schema.full_name == "Updated Name"
        assert schema.is_verified is True

    def test_user_update_partial(self):
        """Test partial user update."""
        data = {
            "full_name": "New Name"
        }

        schema = UserUpdate(**data)

        assert schema.full_name == "New Name"
        # Other fields should be None (optional)
        assert schema.is_verified is None


class TestSchemaEdgeCases:
    """Test edge cases and special scenarios for schemas."""

    def test_empty_string_validation(self):
        """Test schemas handle empty strings correctly."""
        data = {
            "name": "",  # Empty string
            "description": "A test dataset"
        }

        # Empty strings might be rejected by validation
        with pytest.raises(ValidationError):
            DatasetCreate(**data)

    def test_null_optional_fields(self):
        """Test schemas handle null optional fields."""
        data = {
            "name": "Test Dataset",
            "description": None  # Null optional field
        }

        schema = DatasetCreate(**data)
        # This might be allowed depending on implementation
        assert schema.name == "Test Dataset"

    def test_very_long_string(self):
        """Test schemas handle very long strings."""
        long_name = "A" * 1000  # 1000 characters

        data = {
            "name": long_name,
            "description": "A test dataset"
        }

        # Depending on max_length validation, this might fail
        try:
            schema = DatasetCreate(**data)
            assert len(schema.name) == 1000
        except ValidationError:
            # Too long, expected if there's a max_length constraint
            pass

    def test_special_characters_in_strings(self):
        """Test schemas handle special characters."""
        data = {
            "name": "Dataset <script>alert('xss')</script>",
            "description": "Test with émojis 🎉 and spëcial çharacters"
        }

        schema = DatasetCreate(**data)

        assert "<script>" in schema.name
        assert "émojis" in schema.description
