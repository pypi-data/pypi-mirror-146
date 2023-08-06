from asyncio import sleep as async_sleep
from threading import Thread


def sync_to_async(_func=None, rate=.001):
    def set_rate(func):
        async def wrapper(*args, **kwargs):
            th = Thread(target=func, args=args, kwargs=kwargs)
            th.start()
            while True:
                if not th.is_alive():
                    break
                await async_sleep(rate)

        return wrapper

    if _func is None:
        return set_rate
    return set_rate(_func)
