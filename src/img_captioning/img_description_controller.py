from src.img_captioning.utils import ImageDescriptionParams
from src.shell_question import ProcessorOption
from src.shell_question import ProcessorOption
from .models import by_cpu, by_gpu

def generate_image_description(
    processor_option: ProcessorOption, params: ImageDescriptionParams
) -> str:
    if processor_option == ProcessorOption.GPU:
        return by_gpu.generate_image_description(params)
    else:
        return by_cpu.generate_image_description(params)