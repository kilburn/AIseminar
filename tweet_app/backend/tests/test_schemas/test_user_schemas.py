import pytest
from pydantic import ValidationError
from app.schemas.user import UserCreate, UserResponse, UserUpdate


class TestUserSchemas:
    """Test user schema validation and serialization."""

    def test_user_create_valid_data(self, sample_user_data):
        """Test UserCreate schema with valid data."""
        user = UserCreate(**sample_user_data)

        assert user.username == sample_user_data["username"]
        assert user.email == sample_user_data["email"]
        assert user.password == sample_user_data["password"]
        assert user.full_name == sample_user_data["full_name"]
        assert user.organization == sample_user_data["organization"]

    def test_user_create_minimum_data(self):
        """Test UserCreate schema with minimum required data."""
        user_data = {
            "username": "testuser",
            "email": "test@example.com",
            "password": "password123"
        }
        user = UserCreate(**user_data)

        assert user.username == "testuser"
        assert user.email == "test@example.com"
        assert user.password == "password123"
        assert user.full_name is None
        assert user.organization is None

    def test_user_create_invalid_username(self):
        """Test UserCreate schema validation for username."""
        # Too short
        with pytest.raises(ValidationError) as exc_info:
            UserCreate(username="ab", email="test@example.com", password="password123")
        assert "min_length" in str(exc_info.value)

        # Too long
        with pytest.raises(ValidationError) as exc_info:
            UserCreate(username="a" * 51, email="test@example.com", password="password123")
        assert "max_length" in str(exc_info.value)

    def test_user_create_invalid_email(self):
        """Test UserCreate schema validation for email."""
        with pytest.raises(ValidationError) as exc_info:
            UserCreate(username="testuser", email="invalid-email", password="password123")
        assert "value is not a valid email address" in str(exc_info.value)

        with pytest.raises(ValidationError) as exc_info:
            UserCreate(username="testuser", email="test@", password="password123")
        assert "value is not a valid email address" in str(exc_info.value)

    def test_user_create_invalid_password(self):
        """Test UserCreate schema validation for password."""
        # Too short
        with pytest.raises(ValidationError) as exc_info:
            UserCreate(username="testuser", email="test@example.com", password="123")
        assert "min_length" in str(exc_info.value)

    def test_user_create_invalid_full_name(self):
        """Test UserCreate schema validation for full_name."""
        with pytest.raises(ValidationError) as exc_info:
            UserCreate(
                username="testuser",
                email="test@example.com",
                password="password123",
                full_name="a" * 101
            )
        assert "max_length" in str(exc_info.value)

    def test_user_create_invalid_organization(self):
        """Test UserCreate schema validation for organization."""
        with pytest.raises(ValidationError) as exc_info:
            UserCreate(
                username="testuser",
                email="test@example.com",
                password="password123",
                organization="a" * 256
            )
        assert "max_length" in str(exc_info.value)

    def test_user_update_partial_data(self):
        """Test UserUpdate schema with partial data."""
        update_data = {"full_name": "Updated Name"}
        user_update = UserUpdate(**update_data)

        assert user_update.full_name == "Updated Name"
        assert user_update.organization is None
        assert user_update.email is None

    def test_user_update_full_data(self):
        """Test UserUpdate schema with all data."""
        update_data = {
            "full_name": "Updated Name",
            "organization": "Updated Org",
            "email": "updated@example.com"
        }
        user_update = UserUpdate(**update_data)

        assert user_update.full_name == "Updated Name"
        assert user_update.organization == "Updated Org"
        assert user_update.email == "updated@example.com"

    def test_user_update_invalid_email(self):
        """Test UserUpdate schema validation for invalid email."""
        with pytest.raises(ValidationError) as exc_info:
            UserUpdate(email="invalid-email")
        assert "value is not a valid email address" in str(exc_info.value)

    def test_user_response_serialization(self):
        """Test UserResponse schema serialization."""
        user_data = {
            "id": "123e4567-e89b-12d3-a456-426614174000",
            "username": "testuser",
            "email": "test@example.com",
            "full_name": "Test User",
            "organization": "Test Org",
            "is_active": True,
            "is_verified": False,
            "created_at": "2024-01-01T00:00:00Z",
            "updated_at": None,
            "last_login": None
        }

        user_response = UserResponse(**user_data)

        assert user_response.id == "123e4567-e89b-12d3-a456-426614174000"
        assert user_response.username == "testuser"
        assert user_response.email == "test@example.com"
        assert user_response.full_name == "Test User"
        assert user_response.organization == "Test Org"
        assert user_response.is_active is True
        assert user_response.is_verified is False
        assert user_response.created_at == "2024-01-01T00:00:00Z"
        assert user_response.updated_at is None
        assert user_response.last_login is None

    def test_user_response_optional_fields(self):
        """Test UserResponse schema with optional fields."""
        user_data = {
            "id": "123e4567-e89b-12d3-a456-426614174000",
            "username": "testuser",
            "email": "test@example.com",
            "is_active": True,
            "is_verified": False,
            "created_at": "2024-01-01T00:00:00Z"
        }

        user_response = UserResponse(**user_data)

        assert user_response.full_name is None
        assert user_response.organization is None
        assert user_response.updated_at is None
        assert user_response.last_login is None

    def test_user_password_exclusion(self, sample_user_data):
        """Test that UserResponse schema doesn't include password."""
        user_create = UserCreate(**sample_user_data)

        # Convert to dict and check that password is not in response schema
        user_dict = user_create.model_dump()
        assert "password" in user_dict

        # UserResponse should not have password field at all
        response_fields = UserResponse.model_fields.keys()
        assert "password" not in response_fields