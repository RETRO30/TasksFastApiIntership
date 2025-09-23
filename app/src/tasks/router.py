from fastapi import APIRouter, Depends, HTTPException
from src.tasks.schemas import TaskIn, Task, RequestTask
import json
from settings import settings, redis_client

router = APIRouter("/tasks")



@router.post("/create")
async def create_task(task: TaskIn) -> Task:
    new_task = Task(**task)
    await redis_client.rpush(f"tasks:{task.executor}", json.dumps(new_task))  
    return new_task

@router.get("/get")
async def get_task(search_task_data: RequestTask) -> Task:
    res = await redis_client.blpop(f"tasks:{search_task_data.executor}", timeout=search_task_data.timeout)
    if res is None:
        raise HTTPException(status_code=404, detail="No task available (timeout)")
    _, task_json = res
    return Task.model_validate_json(task_json)
