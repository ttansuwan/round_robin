from httpx import AsyncClient
import pytest
from unittest.mock import patch

from .conftest import mock_forward_succeed, queue


@pytest.mark.asyncio
async def test_success(async_client: AsyncClient):
    # Get the first instance of the queue
    first_instance = queue.instance_list[0]

    with patch("app.queue.Instance.forward", wraps=mock_forward_succeed):
        response = await async_client.post("/", json={"game": "name"})
        assert response.status_code == 200
        assert response.json() == {"game": "name"}

    # Checking the queue
    assert first_instance.url != queue.instance_list[0].url
    assert first_instance.url == queue.instance_list[-1].url
