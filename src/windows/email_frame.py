from src.windows.email_sender import send_email
from src.windows.utils import calcualte_pil_img_proportional_height
from typing import Any
from collections.abc import Callable
from pathlib import Path
from PIL import Image
import customtkinter as ctk
import tkinter as tk

SUBJECT = "⚠️ Acción sospechosa ⚠️"

IMG_WIDTH = 350
FONT_SIZE = 20
FIELDS_PADDING = 10
FIELDS_HEIGHT = 40
IMG_DESCRIPTION_HEIGHT = 150


def set_email_frame_with_carousel(
    root: ctk.CTk,
    img_paths: list[str | Path],
    img_description: str,
    on_frame_close: Callable[..., Any],
):
    email_frame = ctk.CTkFrame(root, corner_radius=10)

    subject = ctk.CTkLabel(
        email_frame,
        height=FIELDS_HEIGHT,
        fg_color="orange red",
        text=SUBJECT,
        justify=tk.CENTER,
        corner_radius=10,
        font=(None, FONT_SIZE),
    )
    subject.pack(pady=(100, 0), padx=10, fill=tk.X)

    email_entry = ctk.CTkEntry(
        email_frame,
        placeholder_text="participante@gmail.com",
        border_width=0,
        fg_color="gray10",
        height=FIELDS_HEIGHT,
        font=(None, FONT_SIZE),
    )
    email_entry.pack(pady=FIELDS_PADDING, padx=10, fill=tk.X)

    carousel_frame = ctk.CTkFrame(email_frame, fg_color="transparent")
    carousel_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    img_index = [0]

    def update_image():
        img_path = img_paths[img_index[0]]
        image = Image.open(img_path)
        image_height = calcualte_pil_img_proportional_height(image, IMG_WIDTH)
        image = ctk.CTkImage(image, None, size=(IMG_WIDTH, image_height))
        image_label.configure(image=image)
        image_label.image = image  # type: ignore

    def next_image():
        img_index[0] = (img_index[0] + 1) % len(img_paths)
        update_image()

    def prev_image():
        img_index[0] = (img_index[0] - 1) % len(img_paths)
        update_image()

    prev_button = ctk.CTkButton(
        carousel_frame,
        text="◀",
        width=30,
        height=30,
        fg_color="blue",
        hover_color="dodger blue",
        command=prev_image,
    )
    prev_button.pack(side=tk.LEFT, padx=(0, 10))

    image_label = ctk.CTkLabel(carousel_frame, text="")
    image_label.pack(side=tk.LEFT, expand=True)

    next_button = ctk.CTkButton(
        carousel_frame,
        text="▶",
        width=30,
        height=30,
        fg_color="blue",
        hover_color="dodger blue",
        command=next_image,
    )
    next_button.pack(side=tk.LEFT, padx=(10, 0))

    update_image()

    image_description = ctk.CTkTextbox(
        email_frame,
        height=IMG_DESCRIPTION_HEIGHT,
        fg_color="gray10",
        border_width=0,
        font=(None, FONT_SIZE),
    )
    image_description.insert("0.0", img_description)
    image_description.configure(state="disabled")
    image_description.pack(pady=FIELDS_PADDING, padx=10, fill=tk.X)

    button_frame = ctk.CTkFrame(email_frame, fg_color="transparent")
    button_frame.pack(pady=20)

    cancel_button = ctk.CTkButton(
        button_frame,
        text="Cancelar",
        fg_color="gray25",
        hover_color="gray20",
        width=80,
        height=35,
        corner_radius=5,
        command=lambda: (on_frame_close(), email_frame.pack_forget()),
    )
    cancel_button.pack(side=tk.LEFT)

    send_button = ctk.CTkButton(
        button_frame,
        text="Enviar",
        fg_color="blue",
        hover_color="dodger blue",
        width=60,
        height=35,
        corner_radius=5,
        command=lambda: (
            on_frame_close(),
            email_frame.pack_forget(),
            send_email(img_paths, img_description, email_entry.get()),
        ),
    )
    send_button.pack(side=tk.LEFT, padx=(10, 0))

    email_frame.pack(side=tk.LEFT, fill=tk.Y, padx=(10, 0), pady=10)
