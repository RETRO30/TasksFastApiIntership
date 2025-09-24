import uvicorn

from src.auth.router import router as auth_router
from src.tasks.router import router as tasks_router

from fastapi import FastAPI

app = FastAPI()
app.include_router(auth_router)
app.include_router(tasks_router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)