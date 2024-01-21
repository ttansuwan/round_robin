import pytest
import pytest_asyncio
from unittest.mock import patch
from httpx import AsyncClient
from faker import Faker

from app.main import app
from app.queue import Instance, InstanceQueue

# Global faker
Faker.seed(0)
fake = Faker()


def mock_forward_succeed(payload: dict):
    return payload


def mock_foward_fail(payload: dict):
    return None


@pytest.fixture(scope="function")
def instance_queue():
    # Generate multiple instances
    queue = InstanceQueue()

    for i in range(3):
        queue.add(Instance(url=fake.url()))
    return queue


@pytest_asyncio.fixture()
async def async_client():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac
