import json

from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, Query
from src.tasks.schemas import TaskIn, Task
from src.auth.schemas import User
from src.auth.service import get_current_user
from settings import redis_client
from logger import get_logger


router = APIRouter(prefix="/tasks")
log = get_logger("API_TASKS")

@router.post("/create")
async def create_task(task: TaskIn, current_user: Annotated[User, Depends(get_current_user)]) -> Task:
    new_task = Task(**task.model_dump(), customer=current_user.username)
    await redis_client.rpush(f"tasks:{task.executor}", new_task.model_dump_json())  
    log.info(f"New task created: {new_task.executor} {new_task.action}")
    return new_task


@router.get("/get")
async def get_task(timeout: Annotated[int, Query(ge=0, description="Timeout for waiting task")], current_user: Annotated[User, Depends(get_current_user)]) -> Task:
    res = await redis_client.blpop(f"tasks:{current_user.username}", timeout=timeout)
    if res is None:
        raise HTTPException(status_code=404, detail="No task available (timeout)")
    _, task_json = res

    task = Task.model_validate_json(task_json)
    
    if task.is_expired:
        log.warning(f"Task expired: {task.executor} {task.action}")
        raise HTTPException(status_code=404, detail="No task available (timeout)")
    
    log.info(f"Task founded: {task.executor} {task.action}")
    return task
