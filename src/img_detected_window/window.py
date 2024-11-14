import tkinter as tk
from typing import Any
from PIL import Image, ImageTk

window_open = False
email_entry = None

def open_window(image_path: str, image_description: str, send_email_callback: Any):
    global window_open, email_entry, send_email_intermediate
    if window_open:
        return

    window_open = True

    window = tk.Tk()
    window.title("Enviar Correo")
    window.geometry("400x450")

    img = Image.open(image_path)
    img = img.resize((300, 200))
    img_tk = ImageTk.PhotoImage(img)

    img_label = tk.Label(window, image=img_tk)
    img_label.image = img_tk
    img_label.pack(padx=10, pady=10)

    desc_label = tk.Label(window, text="Descripción:")
    desc_label.pack(pady=5)

    description_text = tk.Text(window, height=5, width=40)
    description_text.insert(tk.END, image_description)
    description_text.config(state=tk.DISABLED)
    description_text.pack(padx=10, pady=10)

    email_label = tk.Label(window, text="Correo:")
    email_label.pack(pady=5)

    email_entry = tk.Entry(window, width=40)
    email_entry.pack(padx=10, pady=5)

    def send_email_intermediate():
        email = email_entry.get()
        send_email_callback(email)

    send_button = tk.Button(
        window,
        text="Enviar",
        command=lambda: [send_email_intermediate(), close_window(window)],
    )
    send_button.pack(side=tk.LEFT, padx=20)

    cancel_button = tk.Button(
        window, text="Cancelar", command=lambda: close_window(window)
    )
    cancel_button.pack(side=tk.RIGHT, padx=20)

    window.protocol("WM_DELETE_WINDOW", lambda: close_window(window))
    window.mainloop()

def getEmail():
    return email_entry.get() if email_entry else ""

def close_window(window):
    global window_open
    window_open = False
    window.destroy()
