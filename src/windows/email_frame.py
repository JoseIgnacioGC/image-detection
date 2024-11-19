from src.windows.email_sender import send_email
from src.windows.utils import calcualte_pil_img_proportional_height

from typing import Any
from collections.abc import Callable
from pathlib import Path
from PIL import Image
import customtkinter as ctk
import tkinter as tk

SUBJECT = "⚠️!Hay una amenaza!⚠️"


def set_email_frame(
    root: ctk.CTk,
    img_path: str | Path,
    img_description: str,
    on_fram_close: Callable[..., Any],
):
    email_frame = ctk.CTkFrame(root, corner_radius=10)

    email_entry = ctk.CTkEntry(
        email_frame, placeholder_text="example@gmail.com", border_width=0
    )
    email_entry.pack(pady=5, padx=10, fill=tk.X)

    subject_entry = ctk.CTkEntry(email_frame, border_width=0)
    subject_entry.insert(0, SUBJECT)
    subject_entry.configure(state="disabled")
    subject_entry.pack(pady=5, padx=10, fill=tk.X)

    image = Image.open(img_path)
    IMAGE_WIDTH = 200
    image_height = calcualte_pil_img_proportional_height(image, IMAGE_WIDTH)
    image = ctk.CTkImage(image, None, size=(IMAGE_WIDTH, image_height))

    image_label = ctk.CTkLabel(email_frame, image=image, text="")
    image_label.image = image  # type: ignore
    image_label.pack()

    image_description = ctk.CTkTextbox(email_frame, height=100, border_width=0)
    image_description.insert("0.0", img_description)
    image_description.configure(state="disabled")
    image_description.pack(pady=5, padx=10, fill=tk.BOTH)

    button_frame = ctk.CTkFrame(email_frame, fg_color="transparent")
    button_frame.pack(side=tk.BOTTOM, pady=20)

    send_button = ctk.CTkButton(
        button_frame,
        text="Send",
        fg_color="dodger blue",
        hover_color="deep sky blue",
        width=60,
        height=35,
        corner_radius=100,
        command=lambda: (
            on_fram_close(),
            email_frame.pack_forget(),
            send_email(img_path, img_description, email_entry.get()),
        ),
    )
    send_button.pack(side=tk.LEFT, padx=(0, 10))

    cancel_button = ctk.CTkButton(
        button_frame,
        text="Cancel",
        fg_color="blue",
        hover_color="darkblue",
        width=60,
        height=35,
        corner_radius=100,
        command=lambda: (on_fram_close(), email_frame.pack_forget()),
    )
    cancel_button.pack(side=tk.LEFT, padx=(10, 0))

    email_frame.pack(side=tk.LEFT, fill=tk.Y, padx=(10, 0), pady=10)
