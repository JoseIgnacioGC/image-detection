from src.async_utils import run_in_background
from src.shell_question import ProcessorOption
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Callable
    from src.img_captioning.utils import Img
    from queue import Queue
    from threading import Thread

def initialize_model_generator(
    processor_option: ProcessorOption
)  -> "Callable[[Img], tuple[Thread, Queue[str]]]": 
    generate_model_response: "Callable[[Img], str]"
 
    match processor_option:
        case ProcessorOption.Qwen2_2B:
            from .models import by_qwen2_2b
            generate_model_response = by_qwen2_2b.generate_model_response

    print(f"Model {processor_option.name} ready\n")
    return run_in_background(generate_model_response)

