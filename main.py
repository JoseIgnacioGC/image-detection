from src.img_captioning.generate_description import generate_image_description
from src.img_captioning.charge_model import charge_model
from src.get_images import raw_images
from src.shell_question import get_processor_option

# https://huggingface.co/meta-llama/Llama-3.2-11B-Vision-Instruct

processor_option = get_processor_option()
processor_and_model = charge_model(processor_option)
print("Model ready\n")

for raw_image in raw_images:
    try:
        description = generate_image_description(
            processor_option=processor_option,
            raw_image=raw_image,
            **processor_and_model
        )
    except Exception as e:
        print(e)
    else:
        print(description)
