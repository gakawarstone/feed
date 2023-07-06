import pytest
from redis import Redis
from redis.exceptions import ConnectionError

from app.settings import REDIS_HOST
from app.services.queue import QueueService


async def _async_add(a: int, b: int) -> int:
    return a + b


async def test_get_result():
    try:
        Redis(host=REDIS_HOST).ping()
    except ConnectionError:
        pytest.skip('Redis is unreachable')

    expected_result = 3

    result = await QueueService.put_and_wait_for_result(_async_add, [1, 2])

    assert result == expected_result
