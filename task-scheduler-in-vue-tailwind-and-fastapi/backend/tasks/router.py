from typing import List, Optional
from fastapi import APIRouter, Depends, status, Response, Request, Query, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from datetime import date

from backend import db

from .import schema
from .import services
from .filter_schema import TaskFilterParams


router = APIRouter(
    tags=["Task"],
    prefix='/tasks'
)

# Send a cookie here
@router.get("/cookie")
def create_cookie():
    content = {"message": "Come to the dark side, we have cookies"}
    response = JSONResponse(content=content)
    response.set_cookie(key="fakesession", value="fake-cookie-session-value")
    return response



@router.post('/', status_code=status.HTTP_201_CREATED,
             response_model=schema.TaskBase)
async def create_new_task(request: schema.TaskBase, database: Session = Depends(db.get_db)):
    result = await services.create_new_task(request, database)
    return result


@router.get('/', status_code=status.HTTP_200_OK,
            response_model=List[schema.TaskList])
async def task_list(database: Session = Depends(db.get_db)):
    result = await services.get_task_listing(database)
    return result


@router.get('/{task_id}', status_code=status.HTTP_200_OK, response_model=schema.TaskBase)
async def get_task_by_id(task_id: int, database: Session = Depends(db.get_db)):                            
    return await services.get_task_by_id(task_id, database)


@router.delete('/{task_id}', status_code=status.HTTP_204_NO_CONTENT, response_class=Response)
async def delete_task_by_id(task_id: int,
                                database: Session = Depends(db.get_db)):
    return await services.delete_task_by_id(task_id, database)


@router.patch('/{task_id}', status_code=status.HTTP_200_OK, response_model=schema.TaskBase)
async def update_task_by_id(request: schema.TaskUpdate, task_id: int, database: Session = Depends(db.get_db)):
    return await services.update_task_by_id(request, task_id, database)


# New filtering endpoints
async def get_task_filters(
    search: Optional[str] = Query(None),
    status: Optional[List[str]] = Query(None),
    priority: Optional[List[str]] = Query(None),
    tags: Optional[List[str]] = Query(None),
    due_date_from: Optional[date] = Query(None),
    due_date_to: Optional[date] = Query(None),
    created_date_from: Optional[date] = Query(None),
    created_date_to: Optional[date] = Query(None),
    overdue_only: bool = Query(False),
    completed_only: bool = Query(False),
    sort_by: str = Query("createdDate"),
    sort_order: str = Query("desc"),
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
) -> TaskFilterParams:
    return TaskFilterParams(
        search=search,
        status=status,
        priority=priority,
        tags=tags,
        due_date_from=due_date_from,
        due_date_to=due_date_to,
        created_date_from=created_date_from,
        created_date_to=created_date_to,
        overdue_only=overdue_only,
        completed_only=completed_only,
        sort_by=sort_by,
        sort_order=sort_order,
        page=page,
        page_size=page_size
    )


@router.get('/', response_model=schema.PaginatedTaskResponse)
async def get_filtered_tasks(
    filters: TaskFilterParams = Depends(get_task_filters),
    database: Session = Depends(db.get_db)
):
    try:
        result = await services.get_filtered_tasks(filters, database)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get('/filter-options', response_model=schema.FilterOptionsResponse)
async def get_filter_options_endpoint(
    database: Session = Depends(db.get_db)
):
    try:
        options = await services.get_filter_options(database)
        return options
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))