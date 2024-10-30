from os import name, system
from readchar import readkey, key
from enum import Enum, auto


class ProcessorOption(Enum):
    GPU = auto()
    CPU = auto()


def get_processor_option() -> ProcessorOption:
    is_GPU = True
    while True:
        system(("cls" if name == "nt" else "clear"))
        first_arrow = "<" if is_GPU else " "
        second_arrow = "<" if not is_GPU else " "
        print("Choose an option using the arrow keys:")
        print(
            f"1. GPU (fast/nvidia) {first_arrow}\n2. CPU (slow) {second_arrow}",
        )

        pressed_key = readkey()

        if pressed_key == key.UP or pressed_key == key.DOWN:
            is_GPU = not is_GPU
        elif pressed_key == key.ENTER:
            break

    return ProcessorOption.GPU if is_GPU else ProcessorOption.CPU
