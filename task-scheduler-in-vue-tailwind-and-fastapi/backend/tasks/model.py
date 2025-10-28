from datetime import datetime
from sqlalchemy import Column, String, Text, DateTime, Integer, Enum
from sqlalchemy.dialects.postgresql import ARRAY
from enum import Enum as PyEnum


from backend.db import Base


class PriorityEnum(PyEnum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    URGENT = "urgent"


class Task(Base):
    __tablename__ = "task"

    id = Column(Integer, primary_key=True, autoincrement=True)
    createdDate = Column(DateTime, default=datetime.now)
    dueDate = Column(DateTime, default=datetime.now)
    title = Column(String(50))
    description = Column(Text)
    status = Column(String(50))
    priority = Column(Enum(PriorityEnum), nullable=False, default=PriorityEnum.MEDIUM)
    tags = Column(ARRAY(String), nullable=True, default=[])
    completedDate = Column("completeddate", DateTime, nullable=True)

    @property
    def is_overdue(self) -> bool:
        """Task is overdue if due date has passed and not completed"""
        return (
            self.dueDate is not None
            and self.dueDate < datetime.now()
            and self.status != "completed"
        )

    @property
    def days_until_due(self) -> int:
        """Days remaining until due date"""
        if self.dueDate is None:
            return None
        return (self.dueDate.date() - datetime.now().date()).days

    def __str__(self):
        """String representation of Task"""
        return f"Task(id={self.id}, title='{self.title}', status='{self.status}', priority='{self.priority.value}')"

    def __repr__(self):
        """Representation of Task"""
        return f"<Task(id={self.id}, title='{self.title}', status='{self.status}', priority='{self.priority.value}')>"
