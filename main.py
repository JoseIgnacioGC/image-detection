from src.img_captioning.process_model_response import (
    ModelResponse,
    process_model_response,
)
from src.shell_question import get_processor_option
from src.async_utils import run_in_background
from src.img_captioning.utils import ImageDescriptionParams
from src.capture_image import convert_opencv_to_pil
from src.img_captioning.model_controller import charge_model
from src.img_captioning.img_description_controller import generate_image_description
from src.utils import RESOURCES_DIR, set_timer_in_seconds
from src.img_detected_window.window import open_window
from src.img_detected_window.emails import send_email

from datetime import datetime
import cv2
from queue import Queue
import threading


processor_option = get_processor_option()
processor_and_model = charge_model(processor_option)
print(f"Model {processor_option.name} ready\n")

video_capture = cv2.VideoCapture(0)

panic_mode = False

model_response_queue: Queue[str] = Queue()
model_response = ModelResponse("", is_a_crime=False)

processing_img = False
processing_start_time = datetime.now()
has_one_second_passed = set_timer_in_seconds(1)

image_capture_path_crime = "resources/crimeImage/imagen_criminal.jpg"

overlay_image = cv2.imread(str(RESOURCES_DIR / "crime!!.png"))
overlay_image = cv2.resize(overlay_image, (50, 50))
display_police_emoji = False

while True:
    ret, frame = video_capture.read()
    pressed_key = cv2.waitKey(1) & 0xFF

    if not ret:
        print("no hay camara")
        break
    if pressed_key == ord("q"):
        print("Terminando programa...")
        break

    model_response_raw = ""
    if not model_response_queue.empty():
        model_response_raw = model_response_queue.get()
        processing_start_time = datetime.now()
        processing_img = False

    if model_response_raw != "":
        model_response_raw = model_response_raw
        model_response = process_model_response(model_response_raw)
        print(model_response)
        if model_response.is_a_crime:
            panic_mode = True
            cv2.imwrite(image_capture_path_crime, frame)
            display_police_emoji = True
        else:
            display_police_emoji = False

    if display_police_emoji:
        overlay_height, overlay_width = overlay_image.shape[:2]
        y_offset, x_offset = 10, frame.shape[1] - overlay_width - 10
        y1, y2 = y_offset, y_offset + overlay_height
        x1, x2 = x_offset, x_offset + overlay_width
        frame[y1:y2, x1:x2] = overlay_image

    if panic_mode:
        panic_mode = False

        image_capture_path = str(RESOURCES_DIR / "imagen.png")
        cv2.imwrite(image_capture_path, frame)

        threading.Thread(
            target=open_window,
            args=(
                image_capture_path,
                model_response.image_description,
                lambda: send_email(
                    image_capture_path_crime, model_response.image_description
                ),
            ),
        ).start()

    cv2.imshow("camara", frame)

    if has_one_second_passed(processing_start_time) and not processing_img:
        processing_img = True
        pil_image = convert_opencv_to_pil(frame)
        params = ImageDescriptionParams(pil_image, processor_and_model)

        def process_callback(result: str):
            model_response_queue.put(result)

        run_in_background(
            generate_image_description,
            callback=process_callback,
            processor_option=processor_option,
            params=params,
        )

video_capture.release()
cv2.destroyAllWindows()
