import pytest
import uuid
from datetime import datetime
from app.models.user import User
from app.models.dataset import Dataset, ProcessingStatus


class TestDatasetModel:
    """Test Dataset model functionality."""

    def create_test_user(self, db_session, sample_user_data):
        """Helper to create a test user."""
        user = User(
            username=sample_user_data["username"],
            email=sample_user_data["email"],
            password_hash="hashed_password"
        )
        db_session.add(user)
        db_session.commit()
        db_session.refresh(user)
        return user

    def test_dataset_creation(self, db_session, sample_user_data, sample_dataset_data):
        """Test creating a dataset."""
        user = self.create_test_user(db_session, sample_user_data)

        dataset = Dataset(
            user_id=user.id,
            name=sample_dataset_data["name"],
            description=sample_dataset_data["description"],
            file_name="test_dataset.csv",
            file_path="/uploads/test_dataset.csv",
            file_size=1024,
            file_hash="sha256_hash",
            mime_type="text/csv",
            total_rows=100,
            processed_rows=0,
            failed_rows=0,
            processing_status=ProcessingStatus.PENDING,
            is_public=sample_dataset_data["is_public"],
            settings=sample_dataset_data["settings"]
        )

        db_session.add(dataset)
        db_session.commit()
        db_session.refresh(dataset)

        assert dataset.id is not None
        assert isinstance(dataset.id, uuid.UUID)
        assert dataset.user_id == user.id
        assert dataset.name == sample_dataset_data["name"]
        assert dataset.description == sample_dataset_data["description"]
        assert dataset.file_name == "test_dataset.csv"
        assert dataset.processing_status == ProcessingStatus.PENDING
        assert dataset.total_rows == 100
        assert dataset.processed_rows == 0
        assert dataset.failed_rows == 0
        assert dataset.is_public is False
        assert isinstance(dataset.created_at, datetime)

    def test_dataset_status_transitions(self, db_session, sample_user_data):
        """Test dataset processing status transitions."""
        user = self.create_test_user(db_session, sample_user_data)

        dataset = Dataset(
            user_id=user.id,
            name="Test Dataset",
            file_name="test.csv",
            file_path="/uploads/test.csv",
            file_size=1024,
            file_hash="hash",
            mime_type="text/csv",
            processing_status=ProcessingStatus.PENDING
        )

        db_session.add(dataset)
        db_session.commit()
        db_session.refresh(dataset)

        # Initial status should be PENDING
        assert dataset.processing_status == ProcessingStatus.PENDING

        # Transition to UPLOADING
        dataset.processing_status = ProcessingStatus.UPLOADING
        db_session.commit()
        assert dataset.processing_status == ProcessingStatus.UPLOADING

        # Transition to VALIDATING
        dataset.processing_status = ProcessingStatus.VALIDATING
        db_session.commit()
        assert dataset.processing_status == ProcessingStatus.VALIDATING

        # Transition to PROCESSING
        dataset.processing_status = ProcessingStatus.PROCESSING
        dataset.processing_started_at = datetime.utcnow()
        db_session.commit()
        assert dataset.processing_status == ProcessingStatus.PROCESSING
        assert dataset.processing_started_at is not None

        # Transition to COMPLETED
        dataset.processing_status = ProcessingStatus.COMPLETED
        dataset.processing_completed_at = datetime.utcnow()
        dataset.processed_rows = 100
        db_session.commit()
        assert dataset.processing_status == ProcessingStatus.COMPLETED
        assert dataset.processing_completed_at is not None
        assert dataset.processed_rows == 100

    def test_dataset_progress_tracking(self, db_session, sample_user_data):
        """Test dataset processing progress tracking."""
        user = self.create_test_user(db_session, sample_user_data)

        dataset = Dataset(
            user_id=user.id,
            name="Test Dataset",
            file_name="test.csv",
            file_path="/uploads/test.csv",
            file_size=1024,
            file_hash="hash",
            mime_type="text/csv",
            total_rows=100,
            processed_rows=0,
            failed_rows=0,
            processing_status=ProcessingStatus.PROCESSING
        )

        db_session.add(dataset)
        db_session.commit()
        db_session.refresh(dataset)

        # Initial progress
        assert dataset.total_rows == 100
        assert dataset.processed_rows == 0
        assert dataset.failed_rows == 0

        # Update progress
        dataset.processed_rows = 80
        dataset.failed_rows = 5
        db_session.commit()
        db_session.refresh(dataset)

        assert dataset.processed_rows == 80
        assert dataset.failed_rows == 5

    def test_dataset_error_handling(self, db_session, sample_user_data):
        """Test dataset error handling."""
        user = self.create_test_user(db_session, sample_user_data)

        dataset = Dataset(
            user_id=user.id,
            name="Test Dataset",
            file_name="test.csv",
            file_path="/uploads/test.csv",
            file_size=1024,
            file_hash="hash",
            mime_type="text/csv",
            processing_status=ProcessingStatus.PROCESSING
        )

        db_session.add(dataset)
        db_session.commit()
        db_session.refresh(dataset)

        # Simulate processing error
        dataset.processing_status = ProcessingStatus.FAILED
        dataset.error_message = "Processing failed: Invalid data format"
        db_session.commit()
        db_session.refresh(dataset)

        assert dataset.processing_status == ProcessingStatus.FAILED
        assert dataset.error_message == "Processing failed: Invalid data format"

    def test_dataset_metadata_and_settings(self, db_session, sample_user_data):
        """Test dataset metadata and settings storage."""
        user = self.create_test_user(db_session, sample_user_data)

        metadata = {
            "source": "twitter",
            "collection_date": "2024-01-01",
            "hashtags": ["#AI", "#ML"],
            "language_distribution": {"en": 0.8, "es": 0.2}
        }

        settings = {
            "processing_batch_size": 50,
            "sentiment_threshold": 0.7,
            "remove_duplicates": True,
            "custom_filters": ["spam", "bots"]
        }

        dataset = Dataset(
            user_id=user.id,
            name="Test Dataset",
            file_name="test.csv",
            file_path="/uploads/test.csv",
            file_size=1024,
            file_hash="hash",
            mime_type="text/csv",
            dataset_metadata=metadata,
            settings=settings
        )

        db_session.add(dataset)
        db_session.commit()
        db_session.refresh(dataset)

        assert dataset.dataset_metadata == metadata
        assert dataset.settings == settings

    def test_dataset_public_access(self, db_session, sample_user_data):
        """Test dataset public access control."""
        user = self.create_test_user(db_session, sample_user_data)

        dataset = Dataset(
            user_id=user.id,
            name="Test Dataset",
            file_name="test.csv",
            file_path="/uploads/test.csv",
            file_size=1024,
            file_hash="hash",
            mime_type="text/csv",
            is_public=False
        )

        db_session.add(dataset)
        db_session.commit()
        db_session.refresh(dataset)

        assert dataset.is_public is False

        # Make dataset public
        dataset.is_public = True
        db_session.commit()
        db_session.refresh(dataset)

        assert dataset.is_public is True

    def test_dataset_file_integrity(self, db_session, sample_user_data):
        """Test dataset file integrity tracking."""
        user = self.create_test_user(db_session, sample_user_data)

        dataset = Dataset(
            user_id=user.id,
            name="Test Dataset",
            file_name="test.csv",
            file_path="/uploads/test.csv",
            file_size=2048,
            file_hash="a1b2c3d4e5f6...",  # SHA-256 hash
            mime_type="text/csv",
            encoding="utf-8",
            delimiter=",",
            has_header=True
        )

        db_session.add(dataset)
        db_session.commit()
        db_session.refresh(dataset)

        assert dataset.file_size == 2048
        assert dataset.file_hash == "a1b2c3d4e5f6..."
        assert dataset.mime_type == "text/csv"
        assert dataset.encoding == "utf-8"
        assert dataset.delimiter == ","
        assert dataset.has_header is True