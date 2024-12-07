from ctypes import windll
from src.shell_question import get_processor_option
from src.utils import DATA_DIR, RESOURCES_DIR, make_dirs, set_timer_in_seconds
from src.img_captioning.process_model_response import (
    ModelResponse,
    process_model_response,
)
from src.img_captioning.image_segmentation import segment_person
from src.img_captioning.model_controller import initialize_model_generator
from src.windows.email_frame import set_email_frame
from src.windows.utils import calculate_cv2_img_proportional_height, cv2_to_pil

from ultralytics import YOLO
from datetime import datetime
from queue import Queue
from PIL import Image
import customtkinter as ctk
import cv2
import tkinter as tk


make_dirs()  # Para crear los directorios necesarios
processor_option = get_processor_option()
generate_model_response = initialize_model_generator(processor_option)
has_one_second_passed = set_timer_in_seconds(3)

try:
    yolo_model = YOLO("yolov8n.pt", verbose=False)
except Exception as e:
    raise RuntimeError(f"Error al cargar el modelo YOLOv8: {e}")

image_captured_path = str(DATA_DIR / "images/imagen_criminal.jpg")
overlay_image = cv2.imread(str(RESOURCES_DIR / "images/crime!!.png"))
overlay_image = cv2.resize(overlay_image, (50, 50))

cap = cv2.VideoCapture(0)
ret, frame = cap.read()
if not ret:
    raise Exception("No se pudo acceder a la cámara")

ctk.set_appearance_mode("Dark")  # Modos: "System" (por defecto), "Dark", "Light"
ctk.set_default_color_theme("blue")  # Temas: "blue" (por defecto), "dark-blue", "green"

root = ctk.CTk()
root.title("Cámara Inteligente: detector de crímenes en tiempo real")
root.after(0, lambda: root.state("zoomed"))
root.wm_attributes("-fullscreen", True)

root.iconbitmap("resources/images/icon.ico")
# para tener un icono en la barra de tareas
myappid = "mycompany.myproduct.subproduct.version"
windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

on_closing = lambda: (cap.release(), root.destroy())
root.protocol("WM_DELETE_WINDOW", on_closing)
root.bind("<Escape>", lambda _: on_closing())

WEB_CAM_IMG_WIDTH = 900
web_cam_img_height = calculate_cv2_img_proportional_height(frame, WEB_CAM_IMG_WIDTH)

global_is_email_frame_open = False


def update_webcam(
    root: ctk.CTk,
    camera_label: ctk.CTkLabel,
    model_response_queue: Queue[str],
    model_response: ModelResponse,
    img_processing_start_time: datetime,
    is_img_processing: bool,
    is_panic_mode: bool,
):
    global global_is_email_frame_open

    ret, frame = cap.read()
    if not ret:
        raise Exception("Error al capturar frame de la cámara")

    results = yolo_model(frame)
    detections = results[0].boxes.xyxy.cpu().numpy()
    classes = results[0].boxes.cls.cpu().numpy()

    for i, box in enumerate(detections):
        if int(classes[i]) == 0:  # Clase "persona"
            x1, y1, x2, y2 = map(int, box)
            person_crop = frame[y1:y2, x1:x2]

            segmented_person = segment_person(person_crop)
            frame[y1:y2, x1:x2] = segmented_person

    if not model_response_queue.empty():
        is_img_processing = False

        model_response_raw = model_response_queue.get()
        model_response = process_model_response(model_response_raw)
        is_panic_mode = model_response.is_a_crime
        print(model_response.__dict__)

    if model_response.is_a_crime:
        overlay_height, overlay_width = overlay_image.shape[:2]
        y_offset, x_offset = 10, frame.shape[1] - overlay_width - 10
        y1, y2 = y_offset, y_offset + overlay_height
        x1, x2 = x_offset, x_offset + overlay_width
        frame[y1:y2, x1:x2] = overlay_image

    if is_panic_mode and not global_is_email_frame_open:
        global_is_email_frame_open = True
        is_panic_mode = False

        cv2.imwrite(image_captured_path, frame)

        def on_frame_close():
            globals()["global_is_email_frame_open"] = False

        set_email_frame(
            root,
            image_captured_path,
            model_response.image_description,
            on_frame_close,
        )

    if has_one_second_passed(img_processing_start_time) and not is_img_processing:
        is_img_processing = True
        img_processing_start_time = datetime.now()
        pil_image = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))

        _model_thread, model_response_queue = generate_model_response(pil_image)

    pil_img = cv2_to_pil(frame)
    img_tk = ctk.CTkImage(pil_img, size=(WEB_CAM_IMG_WIDTH, web_cam_img_height))
    camera_label.configure(image=img_tk)
    camera_label.image = img_tk  # type: ignore

    root.after(
        17,
        lambda: update_webcam(
            root,
            camera_label,
            model_response_queue,
            model_response,
            img_processing_start_time,
            is_img_processing,
            is_panic_mode,
        ),
    )


def set_camera_frame(root: ctk.CTk):
    camera_frame = ctk.CTkFrame(root, corner_radius=10)
    camera_label = ctk.CTkLabel(camera_frame, text="")

    camera_label.pack(expand=True, fill=tk.BOTH)
    camera_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)

    update_webcam(
        root,
        camera_label=camera_label,
        model_response_queue=Queue(),
        model_response=ModelResponse(
            image_description="", crime_probability=0, is_a_crime=False
        ),  # Proporcionar crime_probability
        img_processing_start_time=datetime.now(),
        is_img_processing=False,
        is_panic_mode=False,
    )


set_camera_frame(root)
root.mainloop()
