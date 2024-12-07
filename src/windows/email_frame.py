from src.windows.email_sender import send_email
from src.windows.utils import calcualte_pil_img_proportional_height

from typing import Any
from collections.abc import Callable
from pathlib import Path
from PIL import Image
import customtkinter as ctk
import tkinter as tk

SUBJECT = "       ⚠️ Acción sospechosa ⚠️"

IMG_WIDTH = 350
FONT_SIZE = 20
FIELDS_PADDING = 10
FIELDS_HEIGHT = 40
IMG_DESCRIPTION_HEIGHT = 150


def set_email_frame(
    root: ctk.CTk,
    img_path: str | Path,
    img_description: str,
    on_fram_close: Callable[..., Any],
):
    email_frame = ctk.CTkFrame(root, corner_radius=10)

    subject = ctk.CTkTextbox(
        email_frame,
        height=FIELDS_HEIGHT,
        fg_color="orange red",
        font=(None, FONT_SIZE),
    )
    subject.insert("0.0", SUBJECT)
    subject.configure(state="disabled")
    subject.pack(pady=(100, 0), padx=10, fill=tk.X)

    email_entry_frame = ctk.CTkFrame(email_frame, fg_color="transparent")
    email_entry = ctk.CTkEntry(
        email_entry_frame,
        placeholder_text="participante@gmail.com",
        border_width=0,
        fg_color="gray10",
        height=FIELDS_HEIGHT,
        font=(None, FONT_SIZE),
    )
    email_entry.pack(fill=tk.X)
    email_entry_frame.pack(pady=FIELDS_PADDING, padx=10, fill=tk.X)

    image = Image.open(img_path)
    image_height = calcualte_pil_img_proportional_height(image, IMG_WIDTH)
    image = ctk.CTkImage(image, None, size=(IMG_WIDTH, image_height))

    image_label = ctk.CTkLabel(email_frame, image=image, text="")
    image_label.image = image  # type: ignore
    image_label.pack(padx=10, fill=tk.BOTH)

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
        command=lambda: (on_fram_close(), email_frame.pack_forget()),
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
            on_fram_close(),
            email_frame.pack_forget(),
            send_email(img_path, img_description, email_entry.get()),
        ),
    )
    send_button.pack(side=tk.LEFT, padx=(10, 0))

    email_frame.pack(side=tk.LEFT, fill=tk.Y, padx=(10, 0), pady=10)
