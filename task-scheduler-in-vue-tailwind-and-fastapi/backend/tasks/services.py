from fastapi import HTTPException, status
from sqlalchemy import select, and_, or_, func, desc, asc
from sqlalchemy.orm import Session
from typing import List, Dict, Any
from . import model
from .filter_schema import TaskFilterParams
from datetime import datetime


async def create_new_task(request, database) -> model.Task:
    new_task = model.Task(title=request.title, description=request.description, status=request.status,
                            createdDate=datetime.now(), dueDate=request.dueDate)
    database.add(new_task)
    database.commit()
    database.refresh(new_task)
    return new_task


async def get_task_listing(database) -> List[model.Task]:
    tasks = database.query(model.Task).all()
    return tasks


async def get_task_by_id(task_id, database):
    task = database.query(model.Task).filter_by(id=task_id).first()
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="task Not Found !"
        )
    return task


async def delete_task_by_id(task_id, database):
    database.query(model.Task).filter(
        model.Task.id == task_id).delete()
    database.commit()


async def update_task_by_id(request, task_id, database):
    task = database.query(model.Task).filter_by(id=task_id).first()
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="task Not Found !"
        )
    task.title = request.title if request.title else task.title
    task.description = request.description if request.description else task.description
    task.status = request.status if request.status else task.status
    task.dueDate = request.dueDate if request.dueDate else task.dueDate
    task.priority = request.priority if request.priority else task.priority
    task.tags = request.tags if request.tags else task.tags
    if request.status == "completed" and not task.completedDate:
        task.completedDate = datetime.now()
    database.commit()
    database.refresh(task)
    return task


async def get_filtered_tasks(filters: TaskFilterParams, db: Session) -> Dict[str, Any]:
    """Get filtered tasks with pagination"""
    # Build base query
    query = select(model.Task)

    # Apply filters
    conditions = []

    # Search filter
    if filters.search:
        search_term = f"%{filters.search.lower()}%"
        conditions.append(
            or_(
                func.lower(model.Task.title).like(search_term),
                func.lower(model.Task.description).like(search_term)
            )
        )

    # Status filter
    if filters.status:
        conditions.append(model.Task.status.in_(filters.status))

    # Priority filter
    if filters.priority:
        conditions.append(model.Task.priority.in_(filters.priority))

    # Tags filter
    if filters.tags:
        conditions.append(model.Task.tags.overlap(filters.tags))

    # Date range filters
    if filters.due_date_from:
        conditions.append(model.Task.dueDate >= filters.due_date_from)
    if filters.due_date_to:
        conditions.append(model.Task.dueDate <= filters.due_date_to)

    # Quick filters
    if filters.overdue_only:
        conditions.append(
            and_(
                model.Task.dueDate < datetime.utcnow(),
                model.Task.status != 'completed'
            )
        )

    if filters.completed_only:
        conditions.append(model.Task.status == 'completed')

    # Apply conditions
    if conditions:
        query = query.where(and_(*conditions))

    # Get total count
    count_query = select(func.count()).select_from(query.subquery())
    total_count = db.execute(count_query).scalar()

    # Apply sorting
    sort_column = getattr(model.Task, filters.sort_by, model.Task.createdDate)
    if filters.sort_order == "desc":
        query = query.order_by(desc(sort_column))
    else:
        query = query.order_by(asc(sort_column))

    # Apply pagination
    offset = (filters.page - 1) * filters.page_size
    query = query.offset(offset).limit(filters.page_size)

    # Execute query
    tasks = db.execute(query).scalars().all()

    return {
        "tasks": tasks,
        "totalCount": total_count,
        "filteredCount": total_count,
        "page": filters.page,
        "pageSize": filters.page_size,
        "totalPages": (total_count + filters.page_size - 1) // filters.page_size
    }


async def get_filter_options(db: Session) -> Dict[str, List[Dict[str, Any]]]:
    """Get available filter options with counts"""
    # Get status counts
    status_query = select(model.Task.status, func.count(model.Task.id)).group_by(model.Task.status)
    status_results = db.execute(status_query).all()

    # Get priority counts
    priority_query = select(model.Task.priority, func.count(model.Task.id)).group_by(model.Task.priority)
    priority_results = db.execute(priority_query).all()

    # Get tag counts
    tag_query = select(func.unnest(model.Task.tags), func.count(model.Task.id)).group_by(func.unnest(model.Task.tags))
    tag_results = db.execute(tag_query).all()

    return {
        "statuses": [{"value": status, "label": status.title(), "count": count}
                    for status, count in status_results],
        "priorities": [{"value": priority.value, "label": priority.value.title(), "count": count}
                      for priority, count in priority_results],
        "tags": [{"value": tag, "label": tag.title(), "count": count}
                for tag, count in tag_results],
        "dateRanges": {}  # To be implemented
    }