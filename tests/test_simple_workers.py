import pytest
import asyncio
from web_crawler.simple_workers import AsyncWorkers
from unittest.mock import AsyncMock, patch


@pytest.fixture(scope="module")
def event_loop():
    return asyncio.get_event_loop()


# @pytest.mark.asyncio
# @patch.object(AsyncWorkers, "my_func", side_effect=AsyncMock())
# async def test_async_workers(mock_my_func):
#     # mock_my_func.side_effect = Exception(asyncio.CancelledError)
#     async_workers = AsyncWorkers()
#     queue = asyncio.Queue()
#     await queue.put(1)
#     async_workers.queue = queue

#     with pytest.raises(asyncio.CancelledError) as exc_info:
#         worker = asyncio.create_task(async_workers.worker())
#         await async_workers.queue.join()
#         worker.cancel()

#     assert exc_info.type == asyncio.CancelledError
#     assert async_workers.queue.qsize() == 0
#     mock_my_func.assert_awaited_once()


@pytest.mark.asyncio
@patch.object(AsyncWorkers, "my_func", side_effect=AsyncMock())
async def test_worker(mock_my_func):
    async_worker = AsyncWorkers()
    async_worker.num_workers = 1

    # Populate the queue with test data
    for i in [1]:
        await async_worker.queue.put(i)

    worker_task = asyncio.create_task(async_worker.worker(), name="test_worker")

    await asyncio.sleep(2)  # Give some time for the worker to process

    # Cancel the worker task
    worker_task.cancel()
    try:
        await worker_task
    except asyncio.CancelledError:
        pass

    assert (
        async_worker.queue.empty()
    ), "Queue should be empty after processing all items"
    mock_my_func.assert_awaited_once()
