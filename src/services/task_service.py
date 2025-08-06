from functools import lru_cache
from uuid import UUID
from fastapi import Depends
from sqlalchemy import select
from src.db.postgres import get_session
from src.models.task import Task
from src.schemas.task_schemas import TaskCreate, TaskUpdate
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import WebSocket
import json


class TaskService:
    _session: AsyncSession

    def __init__(self, session: AsyncSession, ws_manager: WebSocket = None):
        self._session = session
        self.ws_manager = ws_manager

    async def _broadcast_tasks(self):
        """Отправляет актуальный список задач всем клиентам"""
        tasks = await self.get_tasks()
        if self.ws_manager:
            await self.ws_manager.broadcast(
                json.dumps(
                    {
                        "action": "tasks_updated",
                        "data": [task.to_dict() for task in tasks],
                    }
                )
            )

    async def create_task(self, validated_data: TaskCreate):
        create_task_data = validated_data.model_dump(exclude_unset=True)

        new_task_obj = Task(**create_task_data)
        self._session.add(new_task_obj)
        await self._session.commit()
        await self._session.refresh(new_task_obj)
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

        update_task_data = validated_data.model_dump(exclude_unset=True)

        for key, value in update_task_data.items():
            setattr(task_obj, key, value)
        await self._session.commit()

        return task_obj

    async def delete_task(self, task_id: UUID | str):
        task_obj = (
            (await self._session.execute(select(Task).filter(Task.id == task_id)))
            .scalars()
            .one_or_none()
        )

        if not task_obj:
            return False

        await self._session.delete(task_obj)
        await self._session.commit()

        return True

    async def get_tasks(self):
        task_objs = (await self._session.execute(select(Task))).scalars().all()
        return task_objs


@lru_cache()
def get_task_service(
    session: AsyncSession = Depends(get_session),
) -> TaskService:
    return TaskService(session)
