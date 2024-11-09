import tkinter as tk


# Titulo y dimensiones de la ventana 
def open_Window(enviar_correo):
    ventana = tk.Tk()
    ventana.title("Enviar Correo")
    ventana.geometry("200x100")
    # aca es el texto que va a mostrar 
    texto="¿Quieres enviar el correo?"
    etiqueta = tk.Label(ventana, text=texto)

    etiqueta.pack(padx=10, pady=20)
        
    boton_enviar = tk.Button(ventana, text="Enviar", command=enviar_correo)
    boton_enviar.pack(side=tk.LEFT, padx=20)
    
        
    boton_cancelar = tk.Button(ventana, text="Cancelar", command=ventana.destroy)
    boton_cancelar.pack(side=tk.RIGHT, padx=20)
        
    ventana.mainloop()