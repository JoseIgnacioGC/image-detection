from enum import Enum, auto
from os import system, name
from readchar import readkey, key


class ProcessorOption(Enum):
    LLAMA = auto()
    GPU = auto()
    CPU = auto()


__options = tuple(ProcessorOption)
__descriptions = {
    ProcessorOption.LLAMA: "Llama (accurated)",
    ProcessorOption.GPU: "GPU (fast/nvidia)",
    ProcessorOption.CPU: "CPU (slow)",
}


def __print_options(chosen_option: ProcessorOption):
    print("Choose an option using the arrow keys:\n")
    for i, option in enumerate(__options):
        arrow = "<" if option == chosen_option else " "
        print(f"{i + 1}. {__descriptions[option]} {arrow}")


def get_processor_option() -> ProcessorOption:
    chosen_option: ProcessorOption = __options[0]

    while True:
        system("cls" if name == "nt" else "clear")
        __print_options(chosen_option)

        pressed_key = readkey()
        match pressed_key:
            case key.UP:
                chosen_option = __options[(chosen_option.value + 1) % len(ProcessorOption)]
            case key.DOWN:
                chosen_option = __options[(chosen_option.value) % len(ProcessorOption)]
            case key.ENTER:
                break
            case _: ...

    return chosen_option
