from src.async_utils import run_in_background
from src.img_captioning.utils import ImageDescriptionParams
from src.capture_image import convert_opencv_to_pil
from src.img_captioning.model_controller import charge_model
from src.shell_question import get_processor_option
from src.img_captioning.img_description_controller import generate_image_description

import cv2
from cv2.typing import Scalar
from queue import Queue

processor_option = get_processor_option()
processor_and_model = charge_model(processor_option)
print("Model ready\n")

keywords_theft = (
    "punch",
    "stabbed",
    "danger",
    "scared",
    "knife",
    "pistol",
    "weapon",
    "gun",
)  # no se q mas agregar

video_capture = cv2.VideoCapture(0)

EXIT_TEXT = "<presiona q pa salir>"
EXIT_TEXT_COLOR: Scalar = (255, 255, 255)
FONT_BAND_HEIGHT = 90
FONT_SCALE = 0.6
FONT_THICKNESS = 1

image_description = "Procesando imagen..."
image_description_color: Scalar = (0, 255, 0)
generated_description_queue: Queue[str] = Queue()
processing_img = False

while True:
    ret, frame = video_capture.read()
    pressed_key = cv2.waitKey(1) & 0xFF

    if not ret:
        print("no hay camara")
        break
    if pressed_key == ord("q"):
        print("Terminando programa...")
        break

    if not generated_description_queue.empty():
        image_description = generated_description_queue.get()
        image_description = "\n".join(
            [
                image_description[i : i + 60]
                for i in range(0, len(image_description), 60)
            ]
        )
        processing_img = False

    display_frame = cv2.copyMakeBorder(
        frame, 0, FONT_BAND_HEIGHT, 0, 0, cv2.BORDER_CONSTANT, value=(0, 0, 0)
    )

    y_offset = frame.shape[0] + 20
    lines = image_description.split("\n")
    for line in lines:
        cv2.putText(
            img=display_frame,
            text=line,
            org=(10, y_offset),
            fontFace=cv2.FONT_HERSHEY_SIMPLEX,
            fontScale=FONT_SCALE,
            color=image_description_color,
            thickness=FONT_THICKNESS,
            lineType=cv2.LINE_AA,
        )
        y_offset += 20

    cv2.putText(
        img=display_frame,
        text=EXIT_TEXT,
        org=(10, y_offset),
        fontFace=cv2.FONT_HERSHEY_SIMPLEX,
        fontScale=FONT_SCALE,
        color=EXIT_TEXT_COLOR,
        thickness=FONT_THICKNESS,
        lineType=cv2.LINE_AA,
    )

    cv2.imshow("camara", display_frame)

    if not processing_img:
        processing_img = True
        pil_image = convert_opencv_to_pil(frame)
        params = ImageDescriptionParams(pil_image, processor_and_model)

        def process_callback(result: str):
            generated_description_queue.put(result)

        run_in_background(
            generate_image_description,
            callback=process_callback,
            processor_option=processor_option,
            params=params,
        )

    is_a_thief = any(keyword in image_description for keyword in keywords_theft)
    if is_a_thief:
        image_description_color: Scalar = (0, 0, 255)
    else:
        image_description_color: Scalar = (0, 255, 0)

video_capture.release()
cv2.destroyAllWindows()
