from src.shell_question import get_processor_option
from src.img_captioning.model_controller import charge_model

processor_option = get_processor_option()
processor_and_model = charge_model(processor_option)