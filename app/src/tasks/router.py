import json

from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from src.tasks.schemas import TaskIn, Task, RequestTask
from src.auth.schemas import User
from src.auth.service import get_current_user
from settings import settings, redis_client


router = APIRouter("/tasks")


@router.post("/create")
async def create_task(task: TaskIn, current_user: Annotated[User, Depends(get_current_user)]) -> Task:

    new_task = Task(**task, customer=current_user.username)
    await redis_client.rpush(f"tasks:{task.executor}", json.dumps(new_task))  
    return new_task


@router.get("/get")
async def get_task(search_task_data: RequestTask, current_user: Annotated[User, Depends(get_current_user)]) -> Task:
    res = await redis_client.blpop(f"tasks:{current_user.username}", timeout=search_task_data.timeout)
    if res is None:
        raise HTTPException(status_code=404, detail="No task available (timeout)")
    _, task_json = res

    task = Task.model_validate_json(task_json)

    if task.is_expired():
        raise HTTPException(status_code=404, detail="No task available (timeout)")
    
    return task
