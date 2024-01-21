import pytest
import pytest_asyncio
from unittest.mock import patch
from httpx import AsyncClient

from app.main import app
from app.queue import Instance, InstanceQueue

# Globalize queue
queue = InstanceQueue()

def mock_forward_succeed(payload: dict):
    return payload


def mock_foward_fail(payload: dict):
    return None


@pytest.fixture()
def instance_queue():
    # Generate multiple instances
    instance1 = Instance(url="whatever.com")
    instance2 = Instance(url="next.com")
    instance3 = Instance(url="test.com")

    queue.add(instance1)
    queue.add(instance2)
    queue.add(instance3)

    return queue

@pytest_asyncio.fixture()
async def async_client(instance_queue):
    with patch('app.main.queue', instance_queue):
        async with AsyncClient(app=app, base_url="http://test") as ac:
            yield ac
