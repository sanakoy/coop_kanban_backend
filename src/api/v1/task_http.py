from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException
from src.schemas.task_schemas import TaskCreate, TaskUpdate, TaskView
from src.services.task_service import TaskService, get_task_service


router = APIRouter()


@router.post("", response_model=TaskView)
async def create_task(
    task_data: TaskCreate, service: TaskService = Depends(get_task_service)
):
    """Создание новой задачи"""
    try:
        return await service.create_task(task_data)
    except:
        raise HTTPException(
            status_code=500, detail="Возникла ошибка при создании задачи."
        )


@router.patch("/{task_id}", response_model=TaskView)
async def update_task(
    task_id: UUID,
    task_data: TaskUpdate,
    service: TaskService = Depends(get_task_service),
):
    """Обновление задачи"""

    task = await service.update_task(task_id, task_data)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@router.delete("/{task_id}", status_code=204)
async def delete_task(task_id: UUID, service: TaskService = Depends(get_task_service)):
    """Удаление задачи"""
    if not await service.delete_task(task_id):
        raise HTTPException(status_code=404, detail="Task not found")


@router.get("", response_model=list[TaskView])
async def get_all_tasks(service: TaskService = Depends(get_task_service)):
    """Вывод всех задач"""
    return await service.get_tasks()
