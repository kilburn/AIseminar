# Quickstart Guide: Schedule Filtering Implementation

**Purpose**: This guide provides step-by-step instructions for implementing the schedule filtering feature from start to finish.

## Prerequisites

- Docker and Docker Compose installed
- Git repository checked out on the `001-schedule-filtering` branch
- All development services running (`docker compose up -d`)
- Database migrations up to date

## Step 1: Database Schema Migration

### 1.1 Create Migration File
```bash
# Access backend container
docker compose exec backend bash

# Create new migration
alembic revision --autogenerate -m "Add priority and tags for task filtering"

# Exit container
exit
```

### 1.2 Migration Content
Edit the generated migration file (e.g., `alembic/versions/xxx_add_priority_and_tags.py`):

```python
"""Add priority and tags for task filtering

Revision ID: add_priority_tags_001
Revises: previous_migration_id
Create Date: 2025-01-28

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers
revision = 'add_priority_tags_001'
down_revision = 'previous_migration_id'
branch_labels = None
depends_on = None

def upgrade():
    # Create priority enum
    priority_enum = postgresql.ENUM('low', 'medium', 'high', 'urgent', name='priorityenum')
    priority_enum.create(op.get_bind())

    # Add new columns to task table
    op.add_column('task', sa.Column('priority', priority_enum, nullable=False, server_default='medium'))
    op.add_column('task', sa.Column('tags', postgresql.ARRAY(sa.String()), nullable=True, server_default='{}'))
    op.add_column('task', sa.Column('completeddate', sa.DateTime(), nullable=True))

    # Create indexes for filtering performance
    op.create_index('idx_tasks_status_priority', 'task', ['status', 'priority'])
    op.create_index('idx_tasks_due_date', 'task', ['duedate'], unique=False, postgresql_where=sa.text('duedate IS NOT NULL'))
    op.create_index('idx_tasks_created_date', 'task', ['createddate'])
    op.create_index('idx_tasks_tags', 'task', ['tags'], unique=False, postgresql_using='gin')

    # Create partial indexes for common scenarios
    op.create_index('idx_active_tasks', 'task', ['priority', 'duedate'],
                   postgresql_where=sa.text("status IN ('pending', 'in_progress')"))

def downgrade():
    # Drop indexes
    op.drop_index('idx_active_tasks', 'task')
    op.drop_index('idx_tasks_tags', 'task')
    op.drop_index('idx_tasks_created_date', 'task')
    op.drop_index('idx_tasks_due_date', 'task')
    op.drop_index('idx_tasks_status_priority', 'task')

    # Drop columns
    op.drop_column('task', 'completeddate')
    op.drop_column('task', 'tags')
    op.drop_column('task', 'priority')

    # Drop enum
    priority_enum = postgresql.ENUM('low', 'medium', 'high', 'urgent', name='priorityenum')
    priority_enum.drop(op.get_bind())
```

### 1.3 Run Migration
```bash
# Apply migration
docker compose exec backend alembic upgrade head

# Verify new columns exist
docker compose exec db psql -U scheduler -d scheduler -c "\d task"
```

## Step 2: Backend Implementation

### 2.1 Update Task Model
Edit `backend/tasks/model.py`:

```python
from sqlalchemy import Column, Integer, String, Text, DateTime, Enum, ARRAY
from sqlalchemy.dialects.postgresql import ENUM
from datetime import datetime
import enum

class PriorityEnum(enum.Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    URGENT = "urgent"

class Task(Base):
    __tablename__ = "task"

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)
    status = Column(String(50), nullable=False, default="pending")
    priority = Column(ENUM(PriorityEnum), nullable=False, default=PriorityEnum.MEDIUM)
    tags = Column(ARRAY(String), nullable=True, default=[])
    createdDate = Column(DateTime, nullable=False, default=datetime.utcnow)
    dueDate = Column(DateTime, nullable=True)
    completedDate = Column(DateTime, nullable=True)

    @property
    def is_overdue(self) -> bool:
        if self.dueDate is None or self.status == "completed":
            return False
        return self.dueDate < datetime.utcnow()
```

### 2.2 Create Filter Schemas
Create `backend/tasks/filter_schema.py`:

```python
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

    class Config:
        orm_mode = True
```

### 2.3 Update Task Schemas
Update `backend/tasks/schema.py`:

```python
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class TaskBase(BaseModel):
    title: str
    description: Optional[str] = None
    status: str
    priority: str
    tags: Optional[List[str]] = []
    dueDate: Optional[datetime] = None

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

class TaskResponse(TaskBase):
    id: int
    createdDate: datetime
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
```

### 2.4 Implement Filter Service
Update `backend/tasks/services.py`:

```python
from sqlalchemy import select, and_, or_, func, desc, asc
from sqlalchemy.orm import Session
from datetime import datetime
from .model import Task
from .filter_schema import TaskFilterParams

async def get_filtered_tasks(filters: TaskFilterParams, db: Session) -> dict:
    # Build base query
    query = select(Task)

    # Apply filters
    conditions = []

    # Search filter
    if filters.search:
        search_term = f"%{filters.search.lower()}%"
        conditions.append(
            or_(
                func.lower(Task.title).like(search_term),
                func.lower(Task.description).like(search_term)
            )
        )

    # Status filter
    if filters.status:
        conditions.append(Task.status.in_(filters.status))

    # Priority filter
    if filters.priority:
        conditions.append(Task.priority.in_(filters.priority))

    # Tags filter
    if filters.tags:
        conditions.append(Task.tags.overlap(filters.tags))

    # Date range filters
    if filters.due_date_from:
        conditions.append(Task.dueDate >= filters.due_date_from)
    if filters.due_date_to:
        conditions.append(Task.dueDate <= filters.due_date_to)

    # Quick filters
    if filters.overdue_only:
        conditions.append(
            and_(
                Task.dueDate < datetime.utcnow(),
                Task.status != 'completed'
            )
        )

    if filters.completed_only:
        conditions.append(Task.status == 'completed')

    # Apply conditions
    if conditions:
        query = query.where(and_(*conditions))

    # Get total count
    count_query = select(func.count()).select_from(query.subquery())
    total_count = db.execute(count_query).scalar()

    # Apply sorting
    sort_column = getattr(Task, filters.sort_by, Task.createdDate)
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
        "filteredCount": total_count,  # For now, same as total
        "page": filters.page,
        "pageSize": filters.page_size,
        "totalPages": (total_count + filters.page_size - 1) // filters.page_size
    }

async def get_filter_options(db: Session) -> dict:
    # Get status counts
    status_query = select(Task.status, func.count(Task.id)).group_by(Task.status)
    status_results = db.execute(status_query).all()

    # Get priority counts
    priority_query = select(Task.priority, func.count(Task.id)).group_by(Task.priority)
    priority_results = db.execute(priority_query).all()

    # Get tag counts
    tag_query = select(func.unnest(Task.tags), func.count(Task.id)).group_by(func.unnest(Task.tags))
    tag_results = db.execute(tag_query).all()

    return {
        "statuses": [{"value": status, "label": status.title(), "count": count}
                    for status, count in status_results],
        "priorities": [{"value": priority, "label": priority.title(), "count": count}
                      for priority, count in priority_results],
        "tags": [{"value": tag, "label": tag.title(), "count": count}
                for tag, count in tag_results],
        "dateRanges": {}  # To be implemented
    }
```

### 2.5 Update Router
Update `backend/tasks/router.py`:

```python
from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from ..db import get_db
from .services import get_filtered_tasks, get_filter_options
from .filter_schema import TaskFilterParams
from .schema import PaginatedTaskResponse, FilterOptionsResponse

router = APIRouter(prefix="/tasks", tags=["tasks"])

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

@router.get("/", response_model=PaginatedTaskResponse)
async def get_tasks(
    filters: TaskFilterParams = Depends(get_task_filters),
    db: Session = Depends(get_db)
):
    try:
        result = await get_filtered_tasks(filters, db)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/filter-options", response_model=FilterOptionsResponse)
async def get_filter_options_endpoint(
    db: Session = Depends(get_db)
):
    try:
        options = await get_filter_options(db)
        return options
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
```

## Step 3: Frontend Implementation

### 3.1 Create Filter Component
Create `client/src/components/TaskFilters.vue`:

```vue
<template>
  <div class="bg-white rounded-lg shadow-md p-6 mb-6">
    <!-- Search Bar -->
    <div class="mb-4">
      <input
        v-model="filters.search"
        @input="debouncedApplyFilters"
        type="text"
        placeholder="Search tasks..."
        class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
      />
    </div>

    <!-- Active Filters -->
    <div v-if="hasActiveFilters" class="flex flex-wrap gap-2 mb-4">
      <span
        v-for="filter in activeFilters"
        :key="filter.key"
        class="inline-flex items-center px-3 py-1 rounded-full text-sm bg-blue-100 text-blue-800"
      >
        {{ filter.label }}
        <button @click="removeFilter(filter.key)" class="ml-2 hover:text-blue-600">
          ×
        </button>
      </span>
      <button @click="resetFilters" class="text-sm text-gray-500 hover:text-gray-700">
        Clear all
      </button>
    </div>

    <!-- Filter Controls -->
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
      <!-- Status Filter -->
      <div>
        <label class="block text-sm font-medium text-gray-700 mb-2">Status</label>
        <select
          v-model="filters.status"
          @change="applyFilters"
          multiple
          class="w-full px-3 py-2 border border-gray-300 rounded-md"
        >
          <option v-for="option in filterOptions.statuses" :key="option.value" :value="option.value">
            {{ option.label }} ({{ option.count }})
          </option>
        </select>
      </div>

      <!-- Priority Filter -->
      <div>
        <label class="block text-sm font-medium text-gray-700 mb-2">Priority</label>
        <select
          v-model="filters.priority"
          @change="applyFilters"
          multiple
          class="w-full px-3 py-2 border border-gray-300 rounded-md"
        >
          <option v-for="option in filterOptions.priorities" :key="option.value" :value="option.value">
            {{ option.label }} ({{ option.count }})
          </option>
        </select>
      </div>

      <!-- Date Range Filter -->
      <div>
        <label class="block text-sm font-medium text-gray-700 mb-2">Due Date Range</label>
        <input
          v-model="filters.dueDateFrom"
          @change="applyFilters"
          type="date"
          class="w-full px-3 py-2 border border-gray-300 rounded-md mb-2"
          placeholder="From"
        />
        <input
          v-model="filters.dueDateTo"
          @change="applyFilters"
          type="date"
          class="w-full px-3 py-2 border border-gray-300 rounded-md"
          placeholder="To"
        />
      </div>

      <!-- Tags Filter -->
      <div>
        <label class="block text-sm font-medium text-gray-700 mb-2">Tags</label>
        <select
          v-model="filters.tags"
          @change="applyFilters"
          multiple
          class="w-full px-3 py-2 border border-gray-300 rounded-md"
        >
          <option v-for="option in filterOptions.tags" :key="option.value" :value="option.value">
            {{ option.label }} ({{ option.count }})
          </option>
        </select>
      </div>
    </div>

    <!-- Quick Filters -->
    <div class="flex gap-2 mt-4">
      <button
        v-for="quickFilter in quickFilters"
        :key="quickFilter.key"
        @click="applyQuickFilter(quickFilter)"
        :class="[
          'px-4 py-2 rounded-md text-sm font-medium transition-colors',
          isQuickFilterActive(quickFilter)
            ? 'bg-blue-600 text-white'
            : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
        ]"
      >
        {{ quickFilter.label }}
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { debounce } from 'lodash-es'
import { useTaskStore } from '@/stores/taskStore'

const taskStore = useTaskStore()

const filters = ref({
  search: '',
  status: [],
  priority: [],
  tags: [],
  dueDateFrom: '',
  dueDateTo: '',
  overdueOnly: false,
  completedOnly: false
})

const filterOptions = ref({
  statuses: [],
  priorities: [],
  tags: []
})

const quickFilters = [
  { key: 'overdue', label: 'Overdue', filter: { overdueOnly: true } },
  { key: 'completed', label: 'Completed', filter: { completedOnly: true } },
  { key: 'today', label: 'Due Today', filter: { dueDateFrom: new Date().toISOString().split('T')[0] } }
]

const hasActiveFilters = computed(() => {
  return Object.values(filters.value).some(value =>
    value !== '' && value !== null && value !== false &&
    (Array.isArray(value) ? value.length > 0 : true)
  )
})

const activeFilters = computed(() => {
  const active = []
  // Build active filters display logic here
  return active
})

const debouncedApplyFilters = debounce(() => {
  applyFilters()
}, 300)

const applyFilters = () => {
  taskStore.updateFilters(filters.value)
}

const removeFilter = (key) => {
  if (Array.isArray(filters.value[key])) {
    filters.value[key] = []
  } else {
    filters.value[key] = ''
  }
  applyFilters()
}

const resetFilters = () => {
  filters.value = {
    search: '',
    status: [],
    priority: [],
    tags: [],
    dueDateFrom: '',
    dueDateTo: '',
    overdueOnly: false,
    completedOnly: false
  }
  applyFilters()
}

const applyQuickFilter = (quickFilter) => {
  Object.assign(filters.value, quickFilter.filter)
  applyFilters()
}

const isQuickFilterActive = (quickFilter) => {
  return Object.entries(quickFilter.filter).every(([key, value]) =>
    filters.value[key] === value
  )
}

onMounted(async () => {
  // Load filter options
  try {
    const options = await taskStore.getFilterOptions()
    filterOptions.value = options
  } catch (error) {
    console.error('Failed to load filter options:', error)
  }
})
</script>
```

### 3.2 Update Task Store
Update `client/src/stores/taskStore.js`:

```javascript
import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { taskApi } from '@/api/tasks'

export const useTaskStore = defineStore('tasks', () => {
  const tasks = ref([])
  const totalCount = ref(0)
  const totalPages = ref(0)
  const loading = ref(false)
  const error = ref(null)

  const filters = ref({
    search: '',
    status: [],
    priority: [],
    tags: [],
    dueDateFrom: '',
    dueDateTo: '',
    overdueOnly: false,
    completedOnly: false,
    sortBy: 'createdDate',
    sortOrder: 'desc',
    page: 1,
    pageSize: 20
  })

  const hasActiveFilters = computed(() => {
    const { search, status, priority, tags, dueDateFrom, dueDateTo, ...rest } = filters.value
    return (
      search !== '' ||
      status.length > 0 ||
      priority.length > 0 ||
      tags.length > 0 ||
      dueDateFrom !== '' ||
      dueDateTo !== '' ||
      Object.values(rest).some(value => value !== false)
    )
  })

  const fetchTasks = async () => {
    loading.value = true
    error.value = null

    try {
      const response = await taskApi.getTasks(filters.value)
      tasks.value = response.tasks
      totalCount.value = response.totalCount
      totalPages.value = response.totalPages
    } catch (err) {
      error.value = err.message || 'Failed to fetch tasks'
      console.error('Error fetching tasks:', err)
    } finally {
      loading.value = false
    }
  }

  const getFilterOptions = async () => {
    try {
      return await taskApi.getFilterOptions()
    } catch (error) {
      console.error('Failed to get filter options:', error)
      throw error
    }
  }

  const updateFilters = (newFilters) => {
    filters.value = { ...filters.value, ...newFilters, page: 1 }
    fetchTasks()
  }

  const resetFilters = () => {
    filters.value = {
      search: '',
      status: [],
      priority: [],
      tags: [],
      dueDateFrom: '',
      dueDateTo: '',
      overdueOnly: false,
      completedOnly: false,
      sortBy: 'createdDate',
      sortOrder: 'desc',
      page: 1,
      pageSize: 20
    }
    fetchTasks()
  }

  return {
    tasks,
    totalCount,
    totalPages,
    loading,
    error,
    filters,
    hasActiveFilters,
    fetchTasks,
    getFilterOptions,
    updateFilters,
    resetFilters
  }
})
```

## Step 4: Integration and Testing

### 4.1 Update Schedule Page
Update the schedule page to include the TaskFilters component:

```vue
<!-- client/src/pages/Scheduler.vue -->
<template>
  <div class="schedule-page">
    <TaskFilters />

    <!-- Task list/calendar view -->
    <div v-if="loading" class="text-center py-8">
      Loading tasks...
    </div>

    <div v-else-if="error" class="text-red-500 py-8">
      Error: {{ error }}
    </div>

    <div v-else>
      <!-- Display filtered tasks -->
      <TaskList :tasks="tasks" />

      <!-- Pagination -->
      <Pagination
        :current-page="currentPage"
        :total-pages="totalPages"
        @page-change="changePage"
      />
    </div>
  </div>
</template>

<script setup>
import { computed, onMounted } from 'vue'
import { useTaskStore } from '@/stores/taskStore'
import TaskFilters from '@/components/TaskFilters.vue'
import TaskList from '@/components/TaskList.vue'
import Pagination from '@/components/Pagination.vue'

const taskStore = useTaskStore()

const tasks = computed(() => taskStore.tasks)
const loading = computed(() => taskStore.loading)
const error = computed(() => taskStore.error)
const currentPage = computed(() => taskStore.filters.page)
const totalPages = computed(() => taskStore.totalPages)

const changePage = (page) => {
  taskStore.updateFilters({ page })
}

onMounted(() => {
  taskStore.fetchTasks()
})
</script>
```

### 4.2 Run Tests
```bash
# Run backend tests
docker compose exec backend python -m pytest

# Run frontend tests (if configured)
docker compose exec frontend npm test
```

### 4.3 Manual Testing Checklist
- [ ] Status filtering works (pending, in_progress, completed)
- [ ] Priority filtering works (low, medium, high, urgent)
- [ ] Date range filtering works
- [ ] Tag filtering works
- [ ] Search functionality works
- [ ] Quick filters work (overdue, completed, today)
- [ ] Multiple filters can be combined
- [ ] Clear all filters works
- [ ] Pagination works with filters
- [ ] Sort options work
- [ ] Performance is acceptable with 1000+ tasks

## Step 5: Deployment

### 5.1 Build and Deploy
```bash
# Build and start services
docker compose -f docker/docker-compose.yaml up --build

# Verify the feature works
curl http://localhost:8080/api/tasks?status=pending&priority=high
```

### 5.2 Monitoring
- Monitor database query performance for filter operations
- Check API response times under load
- Verify filter functionality works across different browsers

## Troubleshooting

### Common Issues
1. **Migration fails**: Check for existing data conflicts or database connection issues
2. **Filter queries are slow**: Verify indexes are created and being used
3. **Frontend not updating**: Check Pinia store integration and reactive properties
4. **API returns errors**: Validate filter parameters and check error handling

### Debug Commands
```bash
# Check database indexes
docker compose exec db psql -U scheduler -d scheduler -c "\d task"

# Check API responses
curl -v "http://localhost:8080/api/tasks?status=pending"

# Check logs
docker compose logs backend
docker compose logs frontend
```

This quickstart guide provides a complete implementation path for the schedule filtering feature, following the established architecture patterns and maintaining consistency with the existing codebase.