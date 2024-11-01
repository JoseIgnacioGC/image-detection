from src.async_utils import run_in_background
from src.img_captioning.utils import ImageDescriptionParams
from src.capture_image import convert_opencv_to_pil
from src.img_captioning.model_controller import charge_model
from src.shell_question import get_processor_option
from src.img_captioning.img_description_controller import generate_image_description
from queue import Queue

import cv2
from cv2.typing import Scalar

processor_option = get_processor_option()
processor_and_model = charge_model(processor_option)
print("Model ready\n")


def capture_image_from_camera():
    cap = cv2.VideoCapture(0)
    font_color: Scalar = (0, 255, 0)
    font_band_height = 90
    font_scale = 0.6
    font_thickness = 1

    processing_img = False

    top_text = "Procesando imagen..."
    buttom_text = "<presiona q pa salir>"
    result_queue: Queue[str] = Queue()

    while True:
        ret, frame = cap.read()
        pressed_key = cv2.waitKey(1) & 0xFF
        if not ret:
            print("no hay camara")
            break
        if pressed_key == ord("q"):
            print("Programa...")
            break

        if not result_queue.empty():
            top_text = result_queue.get()
            top_text = "\n".join(
                [top_text[i : i + 60] for i in range(0, len(top_text), 60)]
            )
            processing_img = False

        display_frame = cv2.copyMakeBorder(
            frame, 0, font_band_height, 0, 0, cv2.BORDER_CONSTANT, value=(0, 0, 0)
        )
        lines = [*top_text.split("\n"), buttom_text]
        y_offset = frame.shape[0] + 20

        for line in lines:
            cv2.putText(
                img=display_frame,
                text=line,
                org=(10, y_offset),
                fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                fontScale=font_scale,
                color=font_color,
                thickness=font_thickness,
                lineType=cv2.LINE_AA,
            )
            y_offset += 20
        cv2.imshow("camara", display_frame)

        if not processing_img:
            processing_img = True
            # buttom_text = "Procesando imagen..."
            pil_image = convert_opencv_to_pil(frame)
            params = ImageDescriptionParams(pil_image, processor_and_model)

            def process_callback(result: str):
                result_queue.put(result)

            run_in_background(
                generate_image_description,
                callback=process_callback,
                processor_option=processor_option,
                params=params,
            )

        keywords_theft = [
            "punch",
            "stabbed",
            "danger",
            "scared",
            "knife",
            "pistol",
            "weapon",
            "gun",
        ]  # no se q mas agregar
        is_a_thief = any(keyword in top_text for keyword in keywords_theft)
        if is_a_thief:
            font_color: Scalar = (0, 0, 255)
        else:
            font_color: Scalar = (0, 255, 0)

    cap.release()
    cv2.destroyAllWindows()


capture_image_from_camera()
