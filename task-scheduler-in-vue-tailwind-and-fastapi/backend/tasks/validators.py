from typing import List
from datetime import datetime

class TaskValidator:
    @staticmethod
    def validate_task_data(data: dict) -> List[str]:
        """Validate task data and return list of errors"""
        errors = []

        # Title validation
        if not data.get('title', '').strip():
            errors.append("Title is required")
        elif len(data.get('title', '').strip()) > 200:
            errors.append("Title must be 200 characters or less")

        # Priority validation
        valid_priorities = ['low', 'medium', 'high', 'urgent']
        if data.get('priority') not in valid_priorities:
            errors.append("Invalid priority value")

        # Status validation
        valid_statuses = ['pending', 'in_progress', 'completed', 'cancelled']
        if data.get('status') not in valid_statuses:
            errors.append("Invalid status value")

        # Date validation
        if data.get('due_date') and data.get('created_date'):
            if data['due_date'] < data['created_date']:
                errors.append("Due date cannot be before created date")

        return errors

class FilterValidator:
    @staticmethod
    def validate_filter_params(data: dict) -> List[str]:
        """Validate filter parameters and return list of errors"""
        errors = []

        # Date range validation
        if data.get('due_date_from') and data.get('due_date_to'):
            if data['due_date_from'] > data['due_date_to']:
                errors.append("Start date cannot be after end date")

        # Pagination validation
        if data.get('page', 1) < 1:
            errors.append("Page must be greater than 0")

        page_size = data.get('page_size', 20)
        if page_size < 1 or page_size > 100:
            errors.append("Page size must be between 1 and 100")

        # Sort validation
        valid_sort_fields = ['createdDate', 'dueDate', 'priority', 'title', 'status']
        if data.get('sort_by') not in valid_sort_fields:
            errors.append(f"Invalid sort field. Must be one of: {', '.join(valid_sort_fields)}")

        return errors