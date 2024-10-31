from src.img_captioning.utils import ProcessorModel
from src.shell_question import ProcessorOption
from .models import by_cpu, by_gpu


def charge_model(
    processor_option: ProcessorOption,
) -> ProcessorModel:
    if processor_option == ProcessorOption.GPU:
        return by_gpu.charge_model()
    else:
        return by_cpu.charge_model()
