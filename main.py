from src.async_utils import run_in_background
from src.img_captioning.utils import ImageDescriptionParams
from src.capture_image import convert_opencv_to_pil
from src.img_captioning.model_controller import charge_model
from src.shell_question import get_processor_option
from src.img_captioning.img_description_controller import generate_image_description

import cv2
from cv2.typing import Scalar
from queue import Queue
import textwrap

processor_option = get_processor_option()
processor_and_model = charge_model(processor_option)
print("Model ready\n")

keywords_theft = (
    "punch", "stabbed", "danger", "scared", "knife", "pistol", "weapon", "gun",
    "robbery", "assault", "fight", "threat", "shout", "scream", "help"
)

video_capture = cv2.VideoCapture(0)
if not video_capture.isOpened():
    print("Error: No se puede acceder a la cámara.")
    exit()

EXIT_TEXT = "<Presiona 'q' para salir>"
EXIT_TEXT_COLOR: Scalar = (255, 255, 255)
FONT_BAND_HEIGHT = 90
FONT_SCALE = 0.6
FONT_THICKNESS = 1

OVERLAY_COLOR = (0, 0, 0)
OVERLAY_ALPHA = 0.5
TEXT_SPACING = 25
PADDING_X = 15

image_description = "Procesando imagen..."
image_description_color: Scalar = (0, 255, 0)
generated_description_queue: Queue[str] = Queue()
processing_img = False

while True:
    ret, frame = video_capture.read()
    pressed_key = cv2.waitKey(1) & 0xFF

    if not ret:
        print("No hay cámara.")
        break
    if pressed_key == ord("q"):
        print("Terminando programa...")
        break

    if not generated_description_queue.empty():
        image_description = generated_description_queue.get()
        image_description = "\n".join(textwrap.wrap(image_description, width=60))
        processing_img = False

    overlay_frame = frame.copy()
    cv2.rectangle(
        overlay_frame,
        (0, frame.shape[0] - FONT_BAND_HEIGHT),
        (frame.shape[1], frame.shape[0]),
        OVERLAY_COLOR,
        -1
    )
    cv2.addWeighted(overlay_frame, OVERLAY_ALPHA, frame, 1 - OVERLAY_ALPHA, 0, frame)

    y_offset = frame.shape[0] - FONT_BAND_HEIGHT + 20
    for line in image_description.split("\n"):
        cv2.putText(
            img=frame,
            text=line,
            org=(PADDING_X, y_offset),
            fontFace=cv2.FONT_HERSHEY_SIMPLEX,
            fontScale=FONT_SCALE,
            color=image_description_color,
            thickness=FONT_THICKNESS,
            lineType=cv2.LINE_AA,
        )
        y_offset += TEXT_SPACING

    cv2.putText(
        img=frame,
        text=EXIT_TEXT,
        org=(PADDING_X, y_offset),
        fontFace=cv2.FONT_HERSHEY_SIMPLEX,
        fontScale=FONT_SCALE,
        color=EXIT_TEXT_COLOR,
        thickness=FONT_THICKNESS,
        lineType=cv2.LINE_AA,
    )

    cv2.imshow("Cámara - Monitoreo", frame)

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
    image_description_color = (0, 0, 255) if is_a_thief else (0, 255, 0)

video_capture.release()
cv2.destroyAllWindows()