from src.img_captioning.utils import ProcessorModel
from src.shell_question import ProcessorOption

def charge_model(
    processor_option: ProcessorOption,
) -> ProcessorModel:
    match processor_option:
        case ProcessorOption.GPU:
            from .models import by_gpu
            return by_gpu.charge_model()
        case ProcessorOption.CPU:
            from .models import by_cpu
            return by_cpu.charge_model()
        case ProcessorOption.LLAMA:
            from .models import by_llama
            return by_llama.charge_model()
        
