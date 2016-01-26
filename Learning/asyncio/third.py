import asyncio

@asyncio.coroutine
def my_coro(future, task_name, seconds_to_sleep=3):
    print('{0} sleeping for: {1}s'.format(task_name, seconds_to_sleep))
    yield from asyncio.sleep(seconds_to_sleep)
    future.set_result('{0} is finished.'.format(task_name))

def got_res(future):
    print(future.result())

loop = asyncio.get_event_loop()
futures = [asyncio.Future() for i in range(2)]

tasks = [my_coro(f, str(i), 3-i) for i, f in enumerate(futures)]

for f in futures: f.add_done_callback(got_res)

loop.run_until_complete(
    asyncio.wait(tasks)
)
loop.close()
