from typing import Optional
from pydantic import Field
from src.models.task import TaskStatus
from src.schemas.base_schemas import BaseOrjsonModel, BaseView


class TaskCreate(BaseOrjsonModel):
    title: str = Field(min_length=2, max_length=100)
    description: str = Field(min_length=2, max_length=500)
    status: TaskStatus


class TaskView(BaseView):
    title: str
    description: str
    status: TaskStatus


class TaskUpdate(BaseOrjsonModel):
    title: str | None = Field(min_length=2, max_length=100)
    description: str | None = Field(min_length=2, max_length=500)
    status: Optional[TaskStatus] = None
