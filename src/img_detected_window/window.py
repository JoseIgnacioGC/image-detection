import tkinter as tk
from typing import Any
from PIL import Image, ImageTk

window_open = False
email_entry = None

font = ("Arial", 12)


def make_description(window: tk.Tk, image_description: str):
    description = description = tk.Label(
        window,
        text=image_description,
        font=font,
        bg="white",
        fg="black",
        wraplength=400,
        justify="center",
    )
    description.pack(pady=(10, 0))


def open_window(image_path: str, image_description: str, send_email_callback: Any):
    global window_open, email_entry, send_email_intermediate
    if window_open:
        return

    window_open = True

    window = tk.Tk()
    window.title("Enviar Correo")
    window.geometry("380x520")
    window.resizable(False, False)

    window.config(bg="white")

    email_entry = tk.Entry(
        window, bd=0, highlightthickness=0, font=font, fg="grey50", width=20
    )
    email_entry.pack(padx=10, ipady=10, fill=tk.X)
    email_entry.insert(0, "example@gmail.com")

    subject_entry = tk.Label(
        window,
        text="Asunto: Se ha detectado un crimen",
        bd=0,
        highlightthickness=0,
        font=font,
        bg="white",
        fg="black",
        anchor="w",
    )
    subject_entry.pack(padx=10, ipady=10, fill=tk.X)

    img = Image.open(image_path)
    img = img.resize((380, 300))
    img_tk = ImageTk.PhotoImage(img)

    img_label = tk.Label(window, image=img_tk)
    img_label.pack()

    make_description(window, image_description)

    def on_focus_in(_: Any) -> None:
        if email_entry.get() == "example@gmail.com":
            email_entry.delete(0, tk.END)
            email_entry.config(fg="black")

    def on_focus_out(_: Any) -> None:
        if email_entry.get() == "":
            email_entry.insert(0, "example@gmail.com")
            email_entry.config(fg="grey")

    email_entry.bind("<FocusIn>", on_focus_in)
    email_entry.bind("<FocusOut>", on_focus_out)

    def send_email_intermediate():
        email = "example@gmail.com" if email_entry is None else email_entry.get()
        send_email_callback(email)

    cancel_button = tk.Button(
        window,
        text="Cancelar",
        width=9,
        highlightthickness=0,
        borderwidth=0,
        background="#0b57d0",
        fg="white",
        font=font,
        command=lambda: close_window(window=window),
    )
    cancel_button.config()
    cancel_button.pack(side=tk.RIGHT, padx=(1, 20), ipady=5)

    send_button = tk.Button(
        window,
        text="Enviar",
        width=8,
        highlightthickness=0,
        borderwidth=0,
        background="#0b57d0",
        fg="white",
        font=font,
        command=lambda: [send_email_intermediate(), close_window(window)],
    )
    send_button.pack(side=tk.RIGHT, ipady=5)

    window.protocol("WM_DELETE_WINDOW", lambda: close_window(window))
    window.mainloop()


def getEmail():
    return email_entry.get() if email_entry else ""


def close_window(window: tk.Tk):
    global window_open
    window_open = False
    window.destroy()
