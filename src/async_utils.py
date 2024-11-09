import threading
from typing import Any
from collections.abc import Callable


def run_in_background(
    func: Callable[..., Any], callback: Callable[[Any], None], *args: Any, **kwargs: Any
) -> threading.Thread:
    def wrapped_func():
        result = func(*args, **kwargs)
        callback(result)

    thread = threading.Thread(target=wrapped_func)
    thread.start()
    return thread
