import threading
from typing import Any
from collections.abc import Callable

def run_in_background(
    func: Callable, callback: Callable[[Any], None], *args, **kwargs
) -> threading.Thread:
    def wrapped_func():
        result = func(*args, **kwargs)
        callback(result)

    thread = threading.Thread(target=wrapped_func)
    thread.start()
    return thread
