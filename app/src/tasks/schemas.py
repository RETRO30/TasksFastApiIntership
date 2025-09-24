from pydantic import BaseModel, Field
from typing import Annotated
from datetime import datetime, timedelta


class TaskIn(BaseModel):
    executor: Annotated[str, Field(description="Id or Name of executor for task")]
    action: Annotated[str, Field(description="Name of action for task")]
    timeout: Annotated[int, Field(description="Timeout for task in seconds")]
    params: Annotated[dict, Field(description="Task parametrs in dictionary")]

class Task(TaskIn):
    customer: Annotated[str, Field(description="Customer who created task")]
    created_at: Annotated[datetime, Field(default_factory=datetime.now, description="UTC timestamp of create task")]

    @property
    def is_expired(self) -> bool:
        return datetime.now() > self.created_at + timedelta(seconds=self.timeout)