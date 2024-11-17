import threading
from queue import Queue
from typing import Any, TypeVar
from collections.abc import Callable
from functools import wraps

T = TypeVar("T")


def run_in_background(
    func: Callable[..., T]
) -> Callable[..., tuple[threading.Thread, Queue[T]]]:
    @wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> tuple[threading.Thread, Queue[T]]:
        response_queue: Queue[T] = Queue()

        def wrapped_func():
            result = func(*args, **kwargs)
            response_queue.put(result)

        thread = threading.Thread(target=wrapped_func)
        thread.start()
        return thread, response_queue

    return wrapper
