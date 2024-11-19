from src.shell_question import get_processor_option
from src.utils import DATA_DIR, RESOURCES_DIR, make_dirs, set_timer_in_seconds
from src.img_captioning.process_model_response import (
    ModelResponse,
    process_model_response,
)

# from src.img_captioning.model_controller import generate_model_response
from src.img_captioning.models.by_fake_model import generate_model_response
from src.windows.email_frame import set_email_frame
from src.windows.utils import calculate_cv2_img_proportional_height, cv2_to_pil

from datetime import datetime
from queue import Queue
import customtkinter as ctk
import cv2
import tkinter as tk
from PIL import Image


make_dirs()
processor_option = get_processor_option()

has_one_second_passed = set_timer_in_seconds(3)
image_captured_path = str(DATA_DIR / "images/imagen_criminal.jpg")
overlay_image = cv2.imread(str(RESOURCES_DIR / "images/crime!!.png"))
overlay_image = cv2.resize(overlay_image, (50, 50))

ctk.set_appearance_mode("Dark")  # Modes: "System" (default), "Dark", "Light"
ctk.set_default_color_theme("blue")  # Themes: "blue" (default), "dark-blue", "green"

root = ctk.CTk()
root.title("Crime Scene Detection")
root.geometry("800x500")
root.resizable(False, False)
# root.iconphoto(False, tk.PhotoImage(file="icon.png"))

cap = cv2.VideoCapture(0)

global_is_email_frame_open = False
IMG_CAMERA_WIDTH = 600


def update_webcam(
    root: ctk.CTk,
    model_response_queue: Queue[str],
    model_response: ModelResponse,
    processing_start_time: datetime,
    display_police_emoji: bool,
    panic_mode: bool,
    processing_img: bool,
):
    global global_is_email_frame_open

    ret, frame = cap.read()
    if not ret:
        raise Exception("Camera not found")

    model_response_raw = ""
    if not model_response_queue.empty():
        model_response_raw = model_response_queue.get()
        processing_start_time = datetime.now()
        processing_img = False

    if model_response_raw != "":
        model_response = process_model_response(model_response_raw)
        print(model_response.__dict__)

        if model_response.is_a_crime:
            panic_mode = True
            display_police_emoji = True
        else:
            display_police_emoji = False

    if display_police_emoji:
        overlay_height, overlay_width = overlay_image.shape[:2]
        y_offset, x_offset = 10, frame.shape[1] - overlay_width - 10
        y1, y2 = y_offset, y_offset + overlay_height
        x1, x2 = x_offset, x_offset + overlay_width
        frame[y1:y2, x1:x2] = overlay_image

    if panic_mode and not global_is_email_frame_open:
        panic_mode = False
        global_is_email_frame_open = True

        cv2.imwrite(image_captured_path, frame)
        image_description = model_response.image_description

        def on_frame_close():
            globals()["is_email_frame_open"] = False

        set_email_frame(
            root,
            image_captured_path,
            image_description,
            on_frame_close,
        )

    if has_one_second_passed(processing_start_time) and not processing_img:
        processing_img = True
        pil_image = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))

        _model_thread, model_response_queue = generate_model_response(
            processor_option, pil_image
        )

    img_camera_height = calculate_cv2_img_proportional_height(frame, IMG_CAMERA_WIDTH)
    pil_img = cv2_to_pil(frame)
    img_tk = ctk.CTkImage(pil_img, size=(IMG_CAMERA_WIDTH, img_camera_height))
    camera_label.configure(image=img_tk)
    camera_label.image = img_tk  # type: ignore

    root.after(
        1,
        lambda: update_webcam(
            root,
            model_response_queue,
            model_response,
            processing_start_time,
            display_police_emoji,
            panic_mode,
            processing_img,
        ),
    )  # loop


def set_camera_frame(root: ctk.CTk):
    camera_frame = ctk.CTkFrame(root, corner_radius=10)

    global camera_label

    camera_label = ctk.CTkLabel(camera_frame, text="")
    camera_label.pack(expand=True, fill=tk.BOTH)
    camera_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)

    update_webcam(
        root,
        model_response_queue=Queue(),
        model_response=ModelResponse("", is_a_crime=False),
        processing_start_time=datetime.now(),
        display_police_emoji=False,
        panic_mode=False,
        processing_img=False,
    )


on_closing = lambda: (cap.release(), root.destroy())
root.protocol("WM_DELETE_WINDOW", on_closing)
root.bind("<Escape>", lambda _: on_closing())

set_camera_frame(root)


root.mainloop()
