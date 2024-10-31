from src.capture_image import capture_image_from_camera
from src.img_captioning.model_controller import charge_model
from src.img_captioning.img_description_controller import generate_image_description
from src.shell_question import get_processor_option


processor_option = get_processor_option()
processor_and_model = charge_model(processor_option)
print("Model ready\n")


raw_image = capture_image_from_camera()

if raw_image:
    try:
        description = generate_image_description(
            processor_option=processor_option,
            raw_image=raw_image,
            **processor_and_model,
        )

        descriptionFile = open("resources/description.txt", "w")
        descriptionFile.write(description)
        descriptionFile.close()

    except Exception as e:
        print(f"Error: {e}")
else:
    print("no se capturo imagen.")
