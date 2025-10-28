import pytest
import uuid
from datetime import datetime
from app.models.user import User


class TestUserModel:
    """Test User model functionality."""

    def test_user_creation(self, db_session, sample_user_data):
        """Test creating a user."""
        user = User(
            username=sample_user_data["username"],
            email=sample_user_data["email"],
            password_hash="hashed_password",
            full_name=sample_user_data["full_name"],
            organization=sample_user_data["organization"]
        )

        db_session.add(user)
        db_session.commit()
        db_session.refresh(user)

        assert user.id is not None
        assert isinstance(user.id, uuid.UUID)
        assert user.username == sample_user_data["username"]
        assert user.email == sample_user_data["email"]
        assert user.full_name == sample_user_data["full_name"]
        assert user.organization == sample_user_data["organization"]
        assert user.is_active is True
        assert user.is_verified is False
        assert isinstance(user.created_at, datetime)
        assert user.updated_at is None

    def test_user_timestamps_on_update(self, db_session, sample_user_data):
        """Test that updated_at timestamp is set on update."""
        user = User(
            username=sample_user_data["username"],
            email=sample_user_data["email"],
            password_hash="hashed_password"
        )

        db_session.add(user)
        db_session.commit()
        db_session.refresh(user)

        # updated_at should be None initially
        assert user.updated_at is None

        # Update user
        user.full_name = "Updated Name"
        db_session.commit()
        db_session.refresh(user)

        # updated_at should now be set
        assert user.updated_at is not None
        assert isinstance(user.updated_at, datetime)

    def test_user_unique_constraints(self, db_session, sample_user_data):
        """Test unique constraints on username and email."""
        # Create first user
        user1 = User(
            username=sample_user_data["username"],
            email=sample_user_data["email"],
            password_hash="hashed_password"
        )

        db_session.add(user1)
        db_session.commit()

        # Try to create second user with same username
        user2 = User(
            username=sample_user_data["username"],
            email="different@example.com",
            password_hash="hashed_password"
        )

        db_session.add(user2)
        with pytest.raises(Exception):  # Should raise IntegrityError
            db_session.commit()

        db_session.rollback()

        # Try to create third user with same email
        user3 = User(
            username="different_user",
            email=sample_user_data["email"],
            password_hash="hashed_password"
        )

        db_session.add(user3)
        with pytest.raises(Exception):  # Should raise IntegrityError
            db_session.commit()

    def test_user_last_login_update(self, db_session, sample_user_data):
        """Test updating last_login timestamp."""
        user = User(
            username=sample_user_data["username"],
            email=sample_user_data["email"],
            password_hash="hashed_password"
        )

        db_session.add(user)
        db_session.commit()
        db_session.refresh(user)

        # Initially last_login should be None
        assert user.last_login is None

        # Update last_login
        login_time = datetime.utcnow()
        user.last_login = login_time
        db_session.commit()
        db_session.refresh(user)

        assert user.last_login is not None
        assert user.last_login == login_time

    def test_user_soft_delete_simulation(self, db_session, sample_user_data):
        """Test simulating soft delete via is_active flag."""
        user = User(
            username=sample_user_data["username"],
            email=sample_user_data["email"],
            password_hash="hashed_password"
        )

        db_session.add(user)
        db_session.commit()
        db_session.refresh(user)

        # User should be active initially
        assert user.is_active is True

        # Deactivate user
        user.is_active = False
        db_session.commit()
        db_session.refresh(user)

        assert user.is_active is False

    def test_user_verification_status(self, db_session, sample_user_data):
        """Test email verification status."""
        user = User(
            username=sample_user_data["username"],
            email=sample_user_data["email"],
            password_hash="hashed_password",
            is_verified=False
        )

        db_session.add(user)
        db_session.commit()
        db_session.refresh(user)

        assert user.is_verified is False

        # Verify user
        user.is_verified = True
        db_session.commit()
        db_session.refresh(user)

        assert user.is_verified is True