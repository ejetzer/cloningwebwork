import asyncio

@asyncio.coroutine
def my_coro(task_name, seconds_to_sleep=3):
    print('{0} sleeping for: {1}s'.format(task_name, seconds_to_sleep))
    yield from asyncio.sleep(seconds_to_sleep)
    print('{0} is finished.'.format(task_name))

loop = asyncio.get_event_loop()
tasks = [
    my_coro('task1', 4),
    my_coro('task2', 3),
    my_coro('task3', 2)
]
loop.run_until_complete(
    asyncio.wait(tasks)
)
loop.close()
