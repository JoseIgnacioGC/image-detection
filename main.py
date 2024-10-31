import cv2
from PIL import Image
from src.shell_question import get_processor_option, ProcessorOption

letterColors = (0, 255, 0)
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
    description = "espacio pa capturar y q pa salir"
    text_band_height = 60
    font_scale = 0.6
    font_thickness = 1

    while True:
        ret, frame = cap.read()
        if not ret:
            print("no hay camara")
            break

        display_frame = cv2.copyMakeBorder(
            frame, 0, text_band_height, 0, 0, cv2.BORDER_CONSTANT, value=(0, 0, 0)
        )
        lines = description.split('\n')
        y_offset = frame.shape[0] + 20

        for line in lines:
            cv2.putText(display_frame, line, (10, y_offset), cv2.FONT_HERSHEY_SIMPLEX,
                        font_scale, letterColors, font_thickness, lineType=cv2.LINE_AA)
            y_offset += 20
        cv2.imshow('camara', display_frame)

        key = cv2.waitKey(1) & 0xFF
        if key == ord(' '):
            pil_image = convert_opencv_to_pil(frame)
            description = generate_image_description(
                processor=processor, model=model, raw_image=pil_image
            )
            description = '\n'.join([description[i:i+60] for i in range(0, len(description), 60)])
        elif key == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

raw_image = capture_image_from_camera()

if raw_image:
    try:
        description = generate_image_description(
            processor=processor, model=model, raw_image=raw_image
        )

        if (["punch", "stabbed", "danger", "scared", "pistol", "weapon"] in description): # no se q mas agregar
            letterColors = (255, 0, 0)

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
