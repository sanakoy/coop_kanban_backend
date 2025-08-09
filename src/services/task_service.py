from functools import lru_cache
from uuid import UUID
from fastapi import Depends, HTTPException
from sqlalchemy import select
from src.websocket.websocket import ws_manager
from src.db.postgres import get_session
from src.models.task import Task
from src.schemas.task_schemas import TaskCreate, TaskUpdate
from sqlalchemy.ext.asyncio import AsyncSession


class TaskService:
    _session: AsyncSession

    def __init__(self, session: AsyncSession):
        self._session = session

    async def _broadcast_tasks(self):
        await ws_manager.broadcast("tasks_updated")

    async def create_task(self, validated_data: TaskCreate):
        create_task_data = validated_data.model_dump(exclude_unset=True)

        new_task_obj = Task(**create_task_data)
        self._session.add(new_task_obj)
        await self._session.commit()
        await self._session.refresh(new_task_obj)
        await self._broadcast_tasks()
        return new_task_obj

    async def update_task(
        self,
        task_id: UUID | str,
        validated_data: TaskUpdate,
    ):
        task_obj = (
            (await self._session.execute(select(Task).filter(Task.id == task_id)))
            .scalars()
            .one_or_none()
        )

        if task_obj is None:
            raise HTTPException(
                status_code=404, detail="Задача с id {} не найдена.".format(task_id)
            )

        update_task_data = validated_data.model_dump(exclude_unset=True)

        try:
            for key, value in update_task_data.items():
                setattr(task_obj, key, value)
            await self._session.commit()
        except:
            raise HTTPException(
                status_code=500,
                detail="Возникла ошибка при обновлении задачи с id {}.".format(task_id),
            )

        await self._broadcast_tasks()

        return task_obj

    async def delete_task(self, task_id: UUID | str):
        task_obj = (
            (await self._session.execute(select(Task).filter(Task.id == task_id)))
            .scalars()
            .one_or_none()
        )

        if task_obj is None:
            raise HTTPException(
                status_code=404, detail="Задача с id {} не найдена.".format(task_id)
            )

        try:
            await self._session.delete(task_obj)
            await self._session.commit()
        except:
            raise HTTPException(
                status_code=500,
                detail="Возникла ошибка при удалении задачи с id {}.".format(task_id),
            )

        await self._broadcast_tasks()
        return True

    async def get_tasks(self):
        task_objs = (await self._session.execute(select(Task))).scalars().all()
        return task_objs


@lru_cache()
def get_task_service(
    session: AsyncSession = Depends(get_session),
) -> TaskService:
    return TaskService(session)
