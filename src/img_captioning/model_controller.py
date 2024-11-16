from src.shell_question import ProcessorOption
from src.img_captioning.utils import Img

def generate_model_response(
    processor_option: ProcessorOption, img: Img
) -> str: 
    match processor_option:
        case ProcessorOption.Qwen2_2B:
            from .models import by_qwen2_2b
            print(f"Model {processor_option.name} ready\n")
            return by_qwen2_2b.generate_image_description(img)
