# Data Model: Schedule Filtering

**Date**: 2025-01-28
**Feature**: Schedule Filtering
**Purpose**: Define enhanced data model for comprehensive task filtering

## Enhanced Task Entity

### Core Task Model
```python
class Task(Base):
    __tablename__ = "task"

    # Existing fields
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)
    status = Column(String(50), nullable=False, default="pending")
    createdDate = Column(DateTime, nullable=False, default=datetime.utcnow)
    dueDate = Column(DateTime, nullable=True)

    # New filtering fields
    priority = Column(Enum(PriorityEnum), nullable=False, default=PriorityEnum.MEDIUM)
    tags = Column(ARRAY(String), nullable=True)
    completedDate = Column(DateTime, nullable=True)

    # Derived/Computed Fields (virtual)
    @property
    def is_overdue(self) -> bool:
        """Task is overdue if due date has passed and not completed"""
        return (
            self.dueDate is not None
            and self.dueDate < datetime.utcnow()
            and self.status != "completed"
        )

    @property
    def days_until_due(self) -> Optional[int]:
        """Days remaining until due date"""
        if self.dueDate is None:
            return None
        return (self.dueDate.date() - datetime.utcnow().date()).days
```

### Priority Enumeration
```python
class PriorityEnum(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    URGENT = "urgent"

    @classmethod
    def get_order_value(cls, priority: str) -> int:
        """Get numeric order for sorting (higher = more urgent)"""
        order_map = {
            cls.LOW: 1,
            cls.MEDIUM: 2,
            cls.HIGH: 3,
            cls.URGENT: 4
        }
        return order_map.get(priority, 2)  # Default to medium
```

### Status Enumeration
```python
class StatusEnum(str, Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"

    @classmethod
    def get_active_statuses(cls) -> List[str]:
        """Get list of statuses considered 'active' (not completed/cancelled)"""
        return [cls.PENDING, cls.IN_PROGRESS]
```

## Filter Query Model

### TaskFilter Entity
```python
class TaskFilter(BaseModel):
    """Model for task filtering parameters"""

    # Search filters
    search: Optional[str] = None

    # Status filters (multi-select allowed)
    status: Optional[List[str]] = None

    # Priority filters (multi-select allowed)
    priority: Optional[List[str]] = None

    # Tag filters (multi-select allowed)
    tags: Optional[List[str]] = None

    # Date range filters
    due_date_from: Optional[datetime] = None
    due_date_to: Optional[datetime] = None
    created_date_from: Optional[datetime] = None
    created_date_to: Optional[datetime] = None

    # Quick filters
    overdue_only: bool = False
    completed_only: bool = False

    # Sorting
    sort_by: str = "createdDate"
    sort_order: str = "desc"

    # Pagination
    page: int = 1
    page_size: int = 20

    class Config:
        orm_mode = True

    def has_active_filters(self) -> bool:
        """Check if any non-default filters are applied"""
        return (
            bool(self.search) or
            bool(self.status) or
            bool(self.priority) or
            bool(self.tags) or
            bool(self.due_date_from) or
            bool(self.due_date_to) or
            self.overdue_only or
            self.completed_only
        )
```

### Filter Result Model
```python
class FilteredTaskResult(BaseModel):
    """Model for filtered task query results"""

    tasks: List[Task]
    total_count: int
    filtered_count: int
    page: int
    page_size: int
    total_pages: int

    # Filter metadata
    applied_filters: TaskFilter
    available_filters: Dict[str, List[str]]  # Available options for each filter type

    class Config:
        orm_mode = True
```

## Database Schema Changes

### Migration Requirements
```sql
-- Create priority enum type
CREATE TYPE priority_enum AS ENUM ('low', 'medium', 'high', 'urgent');

-- Add new columns to task table
ALTER TABLE task
ADD COLUMN priority priority_enum DEFAULT 'medium',
ADD COLUMN tags TEXT[] DEFAULT '{}',
ADD COLUMN completedDate TIMESTAMP;

-- Create indexes for filtering performance
CREATE INDEX idx_tasks_status_priority ON task(status, priority);
CREATE INDEX idx_tasks_due_date ON task(dueDate) WHERE dueDate IS NOT NULL;
CREATE INDEX idx_tasks_created_date ON task(createdDate);
CREATE INDEX idx_tasks_tags ON task USING gin(tags);

-- Partial indexes for common scenarios
CREATE INDEX idx_active_tasks ON task(priority, dueDate)
WHERE status IN ('pending', 'in_progress');

CREATE INDEX idx_overdue_tasks ON task(dueDate, priority)
WHERE dueDate < CURRENT_DATE AND status != 'completed';
```

### Database Constraints
```sql
-- Add constraints for data integrity
ALTER TABLE task
ADD CONSTRAINT chk_priority_valid
CHECK (priority IN ('low', 'medium', 'high', 'urgent'));

ALTER TABLE task
ADD CONSTRAINT chk_due_date_after_created
CHECK (dueDate IS NULL OR dueDate >= createdDate);

ALTER TABLE task
ADD CONSTRAINT chk_completed_date_after_created
CHECK (completedDate IS NULL OR completedDate >= createdDate);
```

## Relationships and Associations

### Task-Category Relationship (Future Enhancement)
```python
# Optional: For more complex categorization
class Category(Base):
    __tablename__ = "category"

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False, unique=True)
    color = Column(String(7), nullable=False)  # Hex color code
    created_at = Column(DateTime, default=datetime.utcnow)

class TaskCategory(Base):
    __tablename__ = "task_category"

    task_id = Column(Integer, ForeignKey("task.id"), primary_key=True)
    category_id = Column(Integer, ForeignKey("category.id"), primary_key=True)
    assigned_at = Column(DateTime, default=datetime.utcnow)
```

### Filter Presets (Future Enhancement)
```python
class FilterPreset(Base):
    __tablename__ = "filter_preset"

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    user_id = Column(Integer, ForeignKey("user.id"))  # If user-specific
    filter_config = Column(JSON, nullable=False)  # Serialized TaskFilter
    created_at = Column(DateTime, default=datetime.utcnow)
    is_default = Column(Boolean, default=False)
```

## Data Validation Rules

### Task Validation
```python
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
```

### Filter Validation
```python
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
```

## Performance Considerations

### Query Optimization
- Use composite indexes for common filter combinations
- Implement partial indexes for frequently accessed subsets
- Use EXPLAIN ANALYZE to verify query performance
- Consider database connection pooling for concurrent filter requests

### Data Volume Considerations
- Paginate all filter results to prevent memory issues
- Implement caching for frequently accessed filter combinations
- Use appropriate data types to minimize storage requirements
- Monitor query performance as task volume grows

This data model provides a solid foundation for implementing comprehensive task filtering while maintaining performance and data integrity.