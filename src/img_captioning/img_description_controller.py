from src.img_captioning.utils import ImageDescriptionParams
from src.shell_question import ProcessorOption
from src.shell_question import ProcessorOption

def generate_image_description(
    processor_option: ProcessorOption, params: ImageDescriptionParams
) -> str:
    match processor_option:
        case ProcessorOption.GPU:
            from .models import  by_gpu
            return by_gpu.generate_image_description(params)
        case ProcessorOption.CPU:
            from .models import by_cpu
            return by_cpu.generate_image_description(params)
        case ProcessorOption.Qwen2_2B:
            from .models import by_qwen2_2b
            return by_qwen2_2b.generate_image_description(params)
