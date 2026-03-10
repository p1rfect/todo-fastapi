from typing import List, Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

import models
import schemas


async def get_task(
    db: AsyncSession,
    task_id: int,
) -> Optional[models.Task]:
    result = await db.execute(
        select(models.Task).where(models.Task.id == task_id)
    )
    return result.scalar_one_or_none()


async def get_tasks(
    db: AsyncSession,
    skip: int = 0,
    limit: int = 100,
) -> List[models.Task]:
    result = await db.execute(
        select(models.Task).offset(skip).limit(limit)
    )
    return result.scalars().all()


async def create_task(
    db: AsyncSession,
    task_in: schemas.TaskCreate,
) -> models.Task:
    db_task = models.Task(
        title=task_in.title,
        description=task_in.description or "",
        completed=False,
    )
    db.add(db_task)
    await db.commit()
    await db.refresh(db_task)
    return db_task


async def update_task(
    db: AsyncSession,
    db_task: models.Task,
    task_in: schemas.TaskUpdate,
) -> models.Task:
    if task_in.title is not None:
        db_task.title = task_in.title
    if task_in.description is not None:
        db_task.description = task_in.description
    if task_in.completed is not None:
        db_task.completed = task_in.completed

    await db.commit()
    await db.refresh(db_task)
    return db_task


async def delete_task(
    db: AsyncSession,
    db_task: models.Task,
) -> None:
    await db.delete(db_task)
    await db.commit()