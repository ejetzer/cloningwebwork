import asyncio

@asyncio.coroutine
def my_coro(seconds_to_sleep=3):
    print('my_coro sleeping for: {0}s'.format(seconds_to_sleep))
    yield from asyncio.sleep(seconds_to_sleep)

loop = asyncio.get_event_loop()
loop.run_until_complete(
    asyncio.gather(my_coro())
)
loop.close()
