from src.get_images import raw_images

from src.img_captioning.by_cpu import (
    generate_image_description,
    get_processor_and_model,
)

processor, model = get_processor_and_model()

for raw_image in raw_images:
    try:
        description = generate_image_description(
            processor=processor, model=model, raw_image=raw_image
        )
    except Exception as e:
        print(e)
    else:
        print(description)

# TODO: give the option to change processor
# from src.shell_question import ProcessorOption, get_processor_option
# processor = get_processor_option()
# if processor == ProcessorOption.GPU:
# import src.img_captioning.by_gpu
# else:
# import src.img_captioning.by_CPU
