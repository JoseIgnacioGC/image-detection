import cv2
from PIL import Image
from src.shell_question import get_processor_option, ProcessorOption

option = get_processor_option()

if option == ProcessorOption.GPU:
    from src.img_captioning.models.by_gpu import (
        generate_image_description,
        get_processor_and_model,
    )
else:
    from src.img_captioning.models.by_cpu import (
        generate_image_description,
        get_processor_and_model,
    )

processor, model = get_processor_and_model()

def convert_opencv_to_pil(cv_image):
    return Image.fromarray(cv2.cvtColor(cv_image, cv2.COLOR_BGR2RGB))

def capture_image_from_camera():
    cap = cv2.VideoCapture(0)

    while True:
        ret, frame = cap.read()
        if not ret:
            print("no hay camara")
            break

        cv2.imshow('espacio pa capturar la foto', frame)


        key = cv2.waitKey(1) & 0xFF
        if key == ord(' '):
            pil_image = convert_opencv_to_pil(frame)
            break
        elif key == ord('q'):
            pil_image = None
            break

    cap.release()
    cv2.destroyAllWindows()
    return pil_image

raw_image = capture_image_from_camera()

if raw_image:
    try:
        description = generate_image_description(
            processor=processor, model=model, raw_image=raw_image
        )

        descriptionFile = open("resources/description.txt", "w")
        descriptionFile.write(description)
        descriptionFile.close()

    except Exception as e:
        print(f"Error: {e}")
else:
    print("no se capturo imagen.")


# TODO: give the option to change processor
# from src.shell_question import ProcessorOption, get_processor_option
# processor = get_processor_option()
# if processor == ProcessorOption.GPU:
# import src.img_captioning.by_gpu
# else:
# import src.img_captioning.by_CPU
