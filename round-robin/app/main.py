from contextlib import asynccontextmanager

from fastapi import FastAPI, Request

from .queue import InstanceQueue, Instance
from .settings import Settings

settings = Settings()
queue = InstanceQueue()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Initialise instance queue alongside with the app
        using FastAPI lifespan
    """

    # Add instances based on the environment setting
    for i in range(settings.NO_INSTANCES):
        queue.add(Instance(url=f"http://coda-instance-demo-{i+1}:8000"))

    yield


app = FastAPI(lifespan=lifespan)


@app.post("/")
async def root(request: Request):
    payload = await request.json()
    response = queue.pop(payload=payload)
    return response
