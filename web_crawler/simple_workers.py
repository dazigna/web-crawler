import asyncio


# Testing class for async workers and queueing system


class AsyncWorkers:
    def __init__(self):
        self.queue = asyncio.Queue()
        self.num_workers = 1

    async def my_func(self, t, name):
        print(f"{name} - started sleeping {t}")
        await asyncio.sleep(t)

        print(f"{name} -finished sleeping {t}")
        self.queue.task_done()

    async def worker_creation(self):
        for i in [4, 1, 3, 2, 8, 9, 7, 1, 5, 3]:
            await self.queue.put(i)
        print(f"Queue size: {self.queue.qsize()}")
        workers = [
            asyncio.create_task(self.worker(), name=f"worker_{i}")
            for i in range(self.num_workers)
        ]
        await self.queue.join()

        for worker in workers:
            worker.cancel()

    async def worker(self):
        print(f"Starting worker {asyncio.current_task().get_name()}")
        while True:
            try:
                print(f"queue size: {self.queue.qsize()}")
                t = await self.queue.get()
                await self.my_func(t, asyncio.current_task().get_name())
            except asyncio.CancelledError:
                print(f"Cancelled worker {asyncio.current_task().get_name()}")
                return
            except Exception as e:
                print(f"Error: {e}")
                return
            finally:
                print(f"Finished worker {asyncio.current_task().get_name()}")

    def main(self):
        asyncio.run(self.worker_creation())


if __name__ == "__main__":
    AsyncWorkers().main()
