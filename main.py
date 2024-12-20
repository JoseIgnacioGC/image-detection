from ctypes import windll
from src.shell_question import get_processor_option
from src.utils import DATA_DIR, make_dirs, set_timer_in_seconds
from src.img_captioning.process_model_response import (
    ModelResponse,
    process_model_response,
)
from src.img_captioning.image_segmentation import segment_person
from src.img_captioning.model_controller import initialize_model_generator
from src.windows.email_frame import set_email_frame_with_carousel
from src.windows.utils import calculate_cv2_img_proportional_height, cv2_to_pil

from datetime import datetime
from queue import Queue
from PIL import Image
import customtkinter as ctk
import cv2
import tkinter as tk
import time

make_dirs()
processor_option = get_processor_option()
generate_model_response = initialize_model_generator(processor_option)
has_one_second_passed = set_timer_in_seconds(3)

cap = cv2.VideoCapture(0)
ret, frame = cap.read()
if not ret:
    raise Exception("No se pudo acceder a la cámara")

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

root = ctk.CTk()
root.title("Cámara Inteligente: Detección de actividades sospechosas")
root.after(0, lambda: root.state("zoomed"))
root.wm_attributes("-fullscreen", True)
root.iconbitmap("resources/images/icon.ico")

myappid = "mycompany.myproduct.subproduct.version"
windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

def close_application():
    cap.release()
    root.destroy()

root.protocol("WM_DELETE_WINDOW", close_application)
root.bind("<Escape>", lambda _: close_application())

WEB_CAM_IMG_WIDTH = 900
web_cam_img_height = calculate_cv2_img_proportional_height(frame, WEB_CAM_IMG_WIDTH)

global_is_email_frame_open = False
captured_images = []

def capture_additional_images(count=2, delay=1):
    for i in range(count):
        time.sleep(delay)
        ret, next_frame = cap.read()
        if not ret:
            continue
        image_path = str(DATA_DIR / f"images/imagen_criminal_{i + 1}.jpg")
        cv2.imwrite(image_path, next_frame)
        captured_images.append(image_path)

def update_webcam(camera_label, model_response_queue, model_response,
                  img_processing_start_time, is_img_processing, is_panic_mode):
    global global_is_email_frame_open

    ret, frame = cap.read()
    if not ret:
        raise Exception("Error al capturar frame de la cámara")

    segmented_frame = segment_person(frame)

    if has_one_second_passed(img_processing_start_time) and not is_img_processing:
        is_img_processing = True
        img_processing_start_time = datetime.now()
        pil_image = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        _, model_response_queue = generate_model_response(pil_image)

    if not model_response_queue.empty():
        is_img_processing = False
        model_response_raw = model_response_queue.get()
        model_response = process_model_response(model_response_raw)
        is_panic_mode = model_response.is_a_crime
        print(model_response.__dict__)

    if is_panic_mode and not global_is_email_frame_open:
        global_is_email_frame_open = True
        is_panic_mode = False

        image_captured_path = str(DATA_DIR / "images/imagen_criminal.jpg")
        cv2.imwrite(image_captured_path, frame)
        captured_images.append(image_captured_path)
        capture_additional_images(count=3, delay=1)

        def on_frame_close():
            global global_is_email_frame_open
            global_is_email_frame_open = False

        set_email_frame_with_carousel(
            root, captured_images, model_response.image_description, on_frame_close
        )

    pil_img = cv2_to_pil(segmented_frame)
    img_tk = ctk.CTkImage(pil_img, size=(WEB_CAM_IMG_WIDTH, web_cam_img_height))
    camera_label.configure(image=img_tk)
    camera_label.image = img_tk

    root.after(17, lambda: update_webcam(
        camera_label, model_response_queue, model_response,
        img_processing_start_time, is_img_processing, is_panic_mode
    ))

def set_camera_frame():
    camera_frame = ctk.CTkFrame(root, corner_radius=10)
    camera_label = ctk.CTkLabel(camera_frame, text="")
    camera_label.pack(expand=True, fill=tk.BOTH)
    camera_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)

    update_webcam(
        camera_label=camera_label,
        model_response_queue=Queue(),
        model_response=ModelResponse(
            image_description="", crime_probability=0, is_a_crime=False
        ),
        img_processing_start_time=datetime.now(),
        is_img_processing=False,
        is_panic_mode=False,
    )

set_camera_frame()
root.mainloop()