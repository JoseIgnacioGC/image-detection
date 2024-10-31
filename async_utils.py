import threading
from typing import Any
from collections.abc import Callable


def run_in_background(
    func: Callable, callback: Callable[[Any], None], *args, **kwargs
) -> threading.Thread:
    """Run function in background thread with callback for result"""

    def wrapped_func():
        result = func(*args, **kwargs)
        callback(result)

    thread = threading.Thread(target=wrapped_func)
    thread.start()
    return thread
