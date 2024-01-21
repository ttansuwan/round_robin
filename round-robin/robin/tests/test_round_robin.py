from httpx import AsyncClient
import pytest
import requests
from unittest.mock import patch, Mock

from .conftest import mock_forward_succeed, mock_foward_fail, instance_queue


class MockResponse:
    """For mocking response from request"""

    def __init__(self, json_data):
        self.json_data = json_data

    def json(self):
        return self.json_data


class TestQueue:
    @pytest.fixture(autouse=True)
    def init(self, instance_queue):
        self.queue = instance_queue

    @pytest.mark.asyncio
    async def test_success(self, async_client: AsyncClient):
        """
        Test from endpoint and how the queue reacts
        """
        # Get the first instance of the queue
        first_instance = self.queue.instance_list[0]

        with patch("app.main.queue", self.queue):
            with patch(
                "app.queue.Instance.forward", wraps=mock_forward_succeed
            ):
                response = await async_client.post("/", json={"game": "name"})
                assert response.status_code == 200
                assert response.json() == {"game": "name"}

        # Checking the queue
        assert first_instance.url != self.queue.instance_list[0].url
        assert first_instance.url == self.queue.instance_list[-1].url

    @pytest.mark.asyncio
    @patch.object(requests, "post")
    async def test_queue_skip_instance(self, mock_post):
        """
        Test when one of the instance is:
            - timeout even after retry
            - any exception (mainly to cover all connection errors)
        """
        # Add mock instance in the queue
        failing_instance = Mock()
        failing_instance.forward.return_value = None
        self.queue.instance_list[0] = failing_instance

        payload = {"something": "something"}

        mock_post.return_value = MockResponse(json_data=payload)
        response = self.queue.pop(payload={"something": "something"})

        assert response == payload
        # Failing instance mock was called once
        failing_instance.forward.assert_called_once()

    @pytest.mark.asyncio
    async def test_queue_empty(self, async_client: AsyncClient):
        """
        Test when all instance lost from endpoint
        """
        with patch("app.main.queue", self.queue):
            with patch("app.queue.Instance.forward", wraps=mock_foward_fail):
                response = await async_client.post("/", json={"game": "name"})
                assert response.status_code == 503
        assert len(self.queue.instance_list) == 0
