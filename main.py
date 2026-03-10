from typing import List

from fastapi import Depends, FastAPI, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

import crud
import schemas
from database import AsyncSessionLocal


app = FastAPI(title="Todo API (async)", version="1.0.0")


async def get_db() -> AsyncSession:
    async with AsyncSessionLocal() as session:
        yield session


@app.get("/tasks", response_model=List[schemas.Task])
async def read_tasks(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db),
):
    tasks = await crud.get_tasks(db, skip=skip, limit=limit)
    return tasks


@app.get("/tasks/{task_id}", response_model=schemas.Task)
async def read_task(
    task_id: int,
    db: AsyncSession = Depends(get_db),
):
    task = await crud.get_task(db, task_id=task_id)
    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found",
        )
    return task


@app.post(
    "/tasks",
    response_model=schemas.Task,
    status_code=status.HTTP_201_CREATED,
)
async def create_task(
    task_in: schemas.TaskCreate,
    db: AsyncSession = Depends(get_db),
):
    task = await crud.create_task(db, task_in=task_in)
    return task


@app.put("/tasks/{task_id}", response_model=schemas.Task)
async def update_task(
    task_id: int,
    task_in: schemas.TaskUpdate,
    db: AsyncSession = Depends(get_db),
):
    task = await crud.get_task(db, task_id=task_id)
    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found",
        )
    task = await crud.update_task(db, db_task=task, task_in=task_in)
    return task


@app.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(
    task_id: int,
    db: AsyncSession = Depends(get_db),
):
    task = await crud.get_task(db, task_id=task_id)
    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found",
        )
    await crud.delete_task(db, db_task=task)
    return None