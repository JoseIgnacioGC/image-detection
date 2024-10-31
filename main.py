from src.img_captioning.utils import ImageDescriptionParams
from src.capture_image import capture_image_from_camera
from src.img_captioning.model_controller import charge_model
from src.img_captioning.img_description_controller import generate_image_description
from src.shell_question import get_processor_option


processor_option = get_processor_option()
processor_and_model = charge_model(processor_option)
print("Model ready\n")


raw_image = capture_image_from_camera()

if not raw_image:
    raise Exception("No image was captured")

params = ImageDescriptionParams(raw_image, processor_and_model)
try:
    description = generate_image_description(
        processor_option=processor_option, params=params
    )
except Exception as e:
    print(f"Error when generating description: {e}")
else:
    with open("resources/description.txt", "w") as descriptionFile:
        descriptionFile.write(description)
