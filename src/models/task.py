from uuid import UUID, uuid4
from enum import Enum
from sqlalchemy import String, Enum as SqlEnum
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.dialects.postgresql import UUID as PG_UUID

class Base(DeclarativeBase):
    """Базовый класс для всех моделей"""
    pass

class TaskStatus(str, Enum):
    TODO = "todo"
    IN_PROGRESS = "in_progress"
    DONE = "done"

class Task(Base):
    __tablename__ = "tasks"

    id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        primary_key=True,
        default=uuid4,
        index=True
    )
    
    title: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        doc="Название задачи"
    )
    
    description: Mapped[str | None] = mapped_column(
        String(500),
        nullable=True,
        doc="Подробное описание задачи"
    )
    
    status: Mapped[TaskStatus] = mapped_column(
        SqlEnum(TaskStatus),
        default=TaskStatus.TODO,
        doc="Текущий статус задачи"
    )

    def __repr__(self):
        return f"Task(id={self.id!r}, title={self.title!r}, status={self.status!r})"