from src.img_captioning.utils import ProcessorModel
from src.shell_question import ProcessorOption

def charge_model(
    processor_option: ProcessorOption,
) -> ProcessorModel:
    match processor_option:
        case ProcessorOption.Qwen2_2B:
            from .models import by_qwen2_2b
            return by_qwen2_2b.charge_model()
        
