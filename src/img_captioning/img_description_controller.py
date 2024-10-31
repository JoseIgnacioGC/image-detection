from PIL import Image
from transformers import BlipProcessor
from transformers.modeling_utils import PreTrainedModel

from src.shell_question import ProcessorOption
from .models import by_cpu, by_gpu


def generate_image_description(
    processor_option: ProcessorOption,
    raw_image: Image,
    processor: BlipProcessor,
    model: PreTrainedModel,
) -> str:
    if processor_option == ProcessorOption.GPU:
        return by_gpu.generate_image_description(raw_image, processor, model=model)
    else:
        return by_cpu.generate_image_description(raw_image, processor, model=model)
