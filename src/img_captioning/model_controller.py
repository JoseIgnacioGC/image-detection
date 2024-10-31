from transformers import BlipProcessor
from transformers.modeling_utils import PreTrainedModel

from src.shell_question import ProcessorOption
from .models import by_cpu, by_gpu


def charge_model(
    processor_option: ProcessorOption,
) -> dict[str, BlipProcessor | PreTrainedModel]:
    if processor_option == ProcessorOption.GPU:
        return by_gpu.charge_model()
    else:
        return by_cpu.charge_model()
