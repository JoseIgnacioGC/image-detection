from src.img_captioning.utils import ImageDescriptionParams
from src.capture_image import convert_opencv_to_pil
from src.img_captioning.model_controller import charge_model
from src.img_captioning.img_description_controller import generate_image_description
from src.shell_question import get_processor_option

import cv2
from cv2.typing import Scalar


processor_option = get_processor_option()
processor_and_model = charge_model(processor_option)
print("Model ready\n")


def capture_image_from_camera():
    cap = cv2.VideoCapture(0)
    letterColors: Scalar = (0, 255, 0)
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
        lines = description.split("\n")
        y_offset = frame.shape[0] + 20

        for line in lines:
            cv2.putText(
                img=display_frame,
                text=line,
                org=(10, y_offset),
                fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                fontScale=font_scale,
                color=letterColors,
                thickness=font_thickness,
                lineType=cv2.LINE_AA,
            )
            y_offset += 20
        cv2.imshow("camara", display_frame)

        key = cv2.waitKey(1) & 0xFF
        if key == ord(" "):
            pil_image = convert_opencv_to_pil(frame)
            params = ImageDescriptionParams(pil_image, processor_and_model)
            description = generate_image_description(
                processor_option=processor_option, params=params
            )
            description = "\n".join(
                [description[i : i + 60] for i in range(0, len(description), 60)]
            )
        elif key == ord("q"):
            break

        keywords_theft = [
            "punch",
            "stabbed",
            "danger",
            "scared",
            "pistol",
            "wepon",
            "gun",
        ]  # no se q mas agregar
        is_a_thief = any(keyword in description for keyword in keywords_theft)
        if is_a_thief:
            letterColors: Scalar = (0, 0, 255)

    cap.release()
    cv2.destroyAllWindows()


capture_image_from_camera()
