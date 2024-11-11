from src.config import processor_option, processor_and_model
from src.async_utils import run_in_background
from src.img_captioning.utils import ImageDescriptionParams
from src.capture_image import convert_opencv_to_pil
from src.img_captioning.img_description_controller import generate_image_description
from src.utils import set_timer_in_seconds
from src.img_detected_window.window import open_window
from src.img_detected_window.emails import send_email

from datetime import datetime
import cv2
from queue import Queue
import threading

def Qwen2_2B_run():
    panic_mode = False
    video_capture = cv2.VideoCapture(0)
    generated_description_queue: Queue[str] = Queue()
    processing_img = False
    processing_start_time = datetime.now()
    has_one_second_passed = set_timer_in_seconds(1)
    overlay_image = cv2.imread("resources/crime!!.png")

    overlay_image = cv2.resize(overlay_image, (50, 50))

    while True:
        ret, frame = video_capture.read()
        pressed_key = cv2.waitKey(1) & 0xFF

        if not ret:
            print("no hay camara")
            break
        if pressed_key == ord("q"):
            print("Terminando programa...")
            break

        image_description = ""
        if not generated_description_queue.empty():
            image_description = generated_description_queue.get()
            processing_start_time = datetime.now()
            processing_img = False

        if image_description != "":
            print(image_description)
            image_description = str(image_description)
            if "True" in image_description or "True. " in image_description:
                panic_mode = True

        if panic_mode:
            overlay_height, overlay_width = overlay_image.shape[:2]
            y_offset, x_offset = 10, frame.shape[1] - overlay_width - 10
            y1, y2 = y_offset, y_offset + overlay_height
            x1, x2 = x_offset, x_offset + overlay_width
            frame[y1:y2, x1:x2] = overlay_image

            image_capture_path = "resources/imagen.png"
            cv2.imwrite(image_capture_path, frame)

            if image_description == "":
                print("esta vacio el mensaje")
            else:
                threading.Thread(
                    target=open_window,
                    args=(image_capture_path, image_description, lambda: send_email(image_capture_path, image_description))
                ).start()

            panic_mode = False

        cv2.imshow("camara", frame)

        if has_one_second_passed(processing_start_time) and not processing_img:
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

    video_capture.release()
    cv2.destroyAllWindows()