from pydantic import BaseModel, Field, validator
from typing import Optional, List
from datetime import datetime, date
from enum import Enum

class PriorityEnum(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    URGENT = "urgent"

class TaskFilterParams(BaseModel):
    search: Optional[str] = Field(None, max_length=200)
    status: Optional[List[str]] = Field(None, min_items=1)
    priority: Optional[List[PriorityEnum]] = Field(None, min_items=1)
    tags: Optional[List[str]] = Field(None, min_items=1)
    due_date_from: Optional[date] = None
    due_date_to: Optional[date] = None
    created_date_from: Optional[date] = None
    created_date_to: Optional[date] = None
    overdue_only: bool = False
    completed_only: bool = False
    sort_by: str = Field("createdDate", regex="^(createdDate|dueDate|priority|title|status)$")
    sort_order: str = Field("desc", regex="^(asc|desc)$")
    page: int = Field(1, ge=1)
    page_size: int = Field(20, ge=1, le=100)

    @validator('due_date_to')
    def validate_date_range(cls, v, values):
        if v and 'due_date_from' in values and values['due_date_from']:
            if v < values['due_date_from']:
                raise ValueError('End date cannot be before start date')
        return v

    @validator('created_date_to')
    def validate_created_date_range(cls, v, values):
        if v and 'created_date_from' in values and values['created_date_from']:
            if v < values['created_date_from']:
                raise ValueError('End date cannot be before start date')
        return v

    class Config:
        orm_mode = True