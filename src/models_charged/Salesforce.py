from src.config import processor_option, processor_and_model
from src.async_utils import run_in_background
from src.img_captioning.utils import ImageDescriptionParams
from src.capture_image import convert_opencv_to_pil
from src.img_captioning.img_description_controller import generate_image_description
from src.utils import set_timer_in_seconds

from datetime import datetime
import cv2
from queue import Queue

def salesforce_run():

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

    #EXIT_TEXT = "<presiona q pa salir>"
    #EXIT_TEXT_COLOR: Scalar = (255, 255, 255)
    #FONT_BAND_HEIGHT = 90
    #FONT_SCALE = 0.6
    #FONT_THICKNESS = 1

    #image_description = "Procesando imagen..."
    #image_description_color: Scalar = (0, 255, 0)

    generated_description_queue: Queue[str] = Queue()
    processing_img = False
    processing_start_time = datetime.now()
    has_one_second_passed = set_timer_in_seconds(1)
    overlay_image = cv2.imread("src/resources/crime!!.png")
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
            #image_description = "\n".join(
            #    [
            #        image_description[i : i + 60]
            #        for i in range(0, len(image_description), 60)
            #    ]
            #)
            processing_start_time = datetime.now()
            processing_img = False


        if image_description != "":
            try:
                print(image_description)
                if "False" in image_description:
                    print("asd")

            except Exception as e:
                print("Error generated:", e)

        overlay_height, overlay_width = overlay_image.shape[:2]

        y_offset, x_offset = 10, frame.shape[1] - overlay_width - 10
        y1, y2 = y_offset, y_offset + overlay_height
        x1, x2 = x_offset, x_offset + overlay_width

        frame[y1:y2, x1:x2] = overlay_image

        #display_frame = cv2.copyMakeBorder(
        #    frame, 0, FONT_BAND_HEIGHT, 0, 0, cv2.BORDER_CONSTANT, value=(0, 0, 0)
        #)

        #y_offset = frame.shape[0] + 20
        #lines = image_description.split("\n")
        #for line in lines:
        #    cv2.putText(
        #        img=display_frame,
        #        text=line,
        #        org=(10, y_offset),
        #        fontFace=cv2.FONT_HERSHEY_SIMPLEX,
        #        fontScale=FONT_SCALE,
        #        color=image_description_color,
        #        thickness=FONT_THICKNESS,
        #        lineType=cv2.LINE_AA,
        #    )
        #    y_offset += 20

        #cv2.putText(
        #    img=display_frame,
        #    text=EXIT_TEXT,
        #    org=(10, y_offset),
        #    fontFace=cv2.FONT_HERSHEY_SIMPLEX,
        #    fontScale=FONT_SCALE,
        #    color=EXIT_TEXT_COLOR,
        #    thickness=FONT_THICKNESS,
        #    lineType=cv2.LINE_AA,
        #)

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

        #is_a_thief = any(keyword in image_description for keyword in keywords_theft)
        #if is_a_thief:
        #    image_description_color: Scalar = (0, 0, 255)
        #else:
        #    image_description_color: Scalar = (0, 255, 0)

    video_capture.release()
    cv2.destroyAllWindows()