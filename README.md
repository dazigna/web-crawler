Concurrency
CPU bound = the time it takes for it to complete is determined principally by the speed of the central processor.

I/O bound - coroutines
 I/O bound refers to a condition in which the time it takes to complete a computation is determined principally by the period spent waiting for input/output operations to be completed

Asyncio

CPU Heavy -> use threading -> threads have over head to spin up
 concurrent.futures


 Asyncio vs concurrent.futres

 going with AsyncIO for concurrency and cooperative multitaksing, using coroutines, low overhead, small tasks to be scheduled, 1000s+

 https://superfastpython.com/threadpoolexecutor-vs-asyncio/




Note: You may be wondering why Python’s requests package isn’t compatible with async IO. requests is built on top of urllib3, which in turn uses Python’s http and socket modules.

By default, socket operations are blocking. This means that Python won’t like await requests.get(url) because .get() is not awaitable. In contrast, almost everything in aiohttp is an awaitable coroutine, such as session.request() and response.text(). It’s a great package otherwise, but you’re doing yourself a disservice by using requests in asynchronous code.


Data storage - insteead of dumping everything at the end we are streaming the content for debugging purposes but also we cna think about doing some double buffering to contain the memory footprint since we are not using a database 

No database because overkill for this small project but if a bigger scale I would use a simple SQlite database and dumb everything into it.


instead of requesting URLs we could request IP directly by taking the DNS record sent back

For dedup we can use a bloom filter A Bloom filter is a probabilistic data structure that allows us to test whether an element is a member of a set. It can tell us definitively if an element is not in the set, but it can only tell us with some probability if an element is in the set. This is perfect for our use case.

Crawler traps
We can add a depth field to our URL table in the Metadata DB and increment this field each time we follow a link. If the depth exceeds a certain threshold, we can stop crawling the page. This will prevent us from getting stuck in a crawler trap.