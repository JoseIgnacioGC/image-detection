from src.windows.utils import calculate_proportional_height

from PIL import Image
import customtkinter as ctk
import tkinter as tk


def get_camera_frame(root: tk.Tk, pil_img: Image.Image) -> ctk.CTkFrame:
    camera_frame = ctk.CTkFrame(root, corner_radius=10)

    # Fixed width for right frame
    RIGHT_WIDTH = 500
    right_height = calculate_proportional_height(pil_img, RIGHT_WIDTH)

    image = ctk.CTkImage(pil_img, None, size=(RIGHT_WIDTH, right_height))

    camera_label = ctk.CTkLabel(camera_frame, image=image, text="")
    camera_label.image = image  # type: ignore
    camera_label.pack(expand=True, fill=tk.BOTH)
    camera_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)

    return camera_frame
