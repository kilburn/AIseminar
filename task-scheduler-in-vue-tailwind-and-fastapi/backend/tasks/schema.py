from datetime import date, datetime
from typing import Optional, List
from pydantic import BaseModel


class TaskBase(BaseModel):
    title: str
    description: Optional[str] = None
    status: str
    priority: str
    tags: Optional[List[str]] = []
    dueDate: Optional[datetime] = None

    class Config:
        orm_mode = True


class TaskCreate(TaskBase):
    pass


class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None
    priority: Optional[str] = None
    tags: Optional[List[str]] = None
    dueDate: Optional[datetime] = None
    completedDate: Optional[datetime] = None

    class Config:
        orm_mode = True


class TaskResponse(TaskBase):
    id: int
    createdDate: datetime
    completedDate: Optional[datetime] = None
    isOverdue: bool = False
    daysUntilDue: Optional[int] = None

    class Config:
        orm_mode = True


class TaskList(BaseModel):
    id: int
    title: str
    description: str
    status: str
    priority: str
    tags: List[str]
    createdDate: datetime
    dueDate: datetime
    completedDate: Optional[datetime] = None
    isOverdue: bool = False
    daysUntilDue: Optional[int] = None

    class Config:
        orm_mode = True


class PaginatedTaskResponse(BaseModel):
    tasks: List[TaskResponse]
    totalCount: int
    filteredCount: int
    page: int
    pageSize: int
    totalPages: int


class FilterOptionsResponse(BaseModel):
    statuses: List[dict]
    priorities: List[dict]
    tags: List[dict]
    dateRanges: dict