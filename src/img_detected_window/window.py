import tkinter as tk
from PIL import Image, ImageTk

window_open = False

def open_window(image_path, image_description, send_email_callback):
    global window_open
    if window_open:
        return

    window_open = True

    window = tk.Tk()
    window.title("Enviar Correo")
    window.geometry("400x400")

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

    boton_enviar = tk.Button(window, text="Enviar", command=lambda: [send_email_callback(), close_window(window)])
    boton_enviar.pack(side=tk.LEFT, padx=20)

    boton_cancelar = tk.Button(window, text="Cancelar", command=lambda: close_window(window))
    boton_cancelar.pack(side=tk.RIGHT, padx=20)

    window.protocol("WM_DELETE_WINDOW", lambda: close_window(window))
    window.mainloop()

def close_window(window):
    global window_open
    window_open = False
    window.destroy()