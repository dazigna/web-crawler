TODO:
Write tradeoffs
Review docstrings
Fix tests


# Web Crawler
A robust asynchronous web crawler built with Python that respects robots.txt and implements rate limiting.

## Features
- 🚀 Asynchronous operation using asyncio
- 🤖 Respects robots.txt rules
- ⏱️ Rate limiting and backoff strategy
- 💾 JSON storage for crawled URLs
- 📊 Logging and monitoring
- 🔄 Automatic retry mechanism


## Usage
Basic usage:

Requires python 3.13

```bash
python web_crawler/web_crawler.py \
    --url https://example.com \
    --workers 5 \
    --max-retries 3 \
    --backoff 5
```

### Command Line Arguments
- `--url`: Starting URL to crawl
- `--workers`: Number of concurrent workers (default: 3)
- `--max-retries`: Maximum retry attempts (default: 3)
- `--backoff`: Backoff time in seconds (default: 5)

## Tests

run test using the following command

```bash
pytest
```

## Technical Details

### Architecture

#### Web crawler 
![web crawler](docs/web_crawler_architecture.jpg "Web crawler architecture")

#### Worker
![Worker](docs/worker.jpg "Worker")

### Trade-offs

### Concurrency
Justify the choice of asyncIO over multirprocessing and threading
- **CPU bound**: Processing time determined by CPU speed
- **I/O bound**: Using coroutines with asyncio for optimal performance

### Why AsyncIO?
- Low overhead
- Cooperative multitasking
- Efficient for handling 1000s+ of small tasks
- Better suited for I/O operations than ThreadPoolExecutor

Define worker pattern used


Use of httpx and not classic requests package:

### Data Storage
Define why use in memory store vs database 
- Simple in-memory storage backed by file I/O

### URL filtering
define the choices , why no normalization

### Content parsing
only href and no dynamic content otherwise we need to execute the links using playwright or selenium or else and beceomes much more complicated for a small time boudnded projects

Crawler traps
not handled

Shared instances of network client and other functional components - ease of mocking and implementation for a time bounded project, none of the utils are storing state and are purely functional
We can decouple each worker util by slightly modifying the implementation to allow each worker to spin up its dependencies and be autonomous

### Logging 
### Optimizations
- DNS record caching
- Bloom filter for URL deduplication
- Better similarity comparision with Jacard or cosine similarity
- Depth tracking for crawler trap prevention
- URL normalization
- Better storage instead of in-memory storage backed by file I/O. Using a proper DB would be better
- Caching of urls for faster lookups, using any classic store such as Redis or Memcache


## License
MIT License


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


Handle normalization
https://discuss.python.org/t/add-uri-normalization-functions-to-the-urllib-parse-module/3799/2


Describe logic

Can add streaming to file

https://url.spec.whatwg.org/#url-class
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


Handle normalization
https://discuss.python.org/t/add-uri-normalization-functions-to-the-urllib-parse-module/3799/2


Describe logic

Can add streaming to file

https://url.spec.whatwg.org/#url-class
