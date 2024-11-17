from src.windows.utils import calculate_proportional_height

from PIL import Image
import customtkinter as ctk
import tkinter as tk


def get_email_frame(root: tk.Tk, pil_img: Image.Image) -> ctk.CTkFrame:
    email_frame = ctk.CTkFrame(root, corner_radius=10)

    email_entry = ctk.CTkEntry(email_frame, placeholder_text="example@gmail.com")
    email_entry.pack(pady=5, padx=10, fill=tk.X)

    subject_entry = ctk.CTkEntry(email_frame)
    subject_entry.insert(0, "subject: A crime was detected")
    subject_entry.configure(state="disabled")
    subject_entry.pack(pady=5, padx=10, fill=tk.X)

    # Fixed width for left frame
    LEFT_WIDTH = 200
    left_height = calculate_proportional_height(pil_img, LEFT_WIDTH)

    image = ctk.CTkImage(pil_img, None, size=(LEFT_WIDTH, left_height))

    photo_label = ctk.CTkLabel(email_frame, image=image, text="")
    photo_label.image = image  # type: ignore
    photo_label.pack()

    photo_description = ctk.CTkTextbox(email_frame, height=100)
    photo_description.insert("0.0", "Description of the image")
    photo_description.configure(state="disabled")
    photo_description.pack(pady=5, padx=10, fill=tk.BOTH)

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
        command=email_frame.pack_forget,
    )
    cancel_button.pack(side=tk.LEFT, padx=(10, 0))
    email_frame.pack(side=tk.LEFT, fill=tk.Y, padx=(10, 0), pady=10)

    return email_frame
