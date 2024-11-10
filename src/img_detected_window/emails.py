from get_env_vars import credentials

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage


def send_email():
    smtp_server = "smtp.gmail.com"
    smtp_port = 465
    username = credentials.email_server_email
    password = credentials.email_server_password

    # Crear el mensaje
    msg = MIMEMultipart()
    msg["From"] = username
    msg["To"] = " "
    msg["Subject"] = "Prueba De Correo"

    Cuerpo_Correo = "Hola buenas tardes"
    msg.attach(MIMEText(Cuerpo_Correo, "plain"))

    # abre la imagen
    imagen_ruta = open("imagenes/pug.png", "rb")

    imagen = MIMEImage(imagen_ruta.read())
    imagen.add_header("Content-Disposition", "attachment", filename="pug.png")
    msg.attach(imagen)
    imagen_ruta.close()

    # Conexión al servidor y envío del correo
    try:
        with smtplib.SMTP_SSL(smtp_server, smtp_port) as server:
            server.login(username, password)
            server.sendmail(msg["From"], msg["To"], msg.as_string())
            print("Correo enviado exitosamente!")
    except Exception as e:
        print(f"Error al enviar correo: {e}")


# use example
# import window
# window.open_window(send_email)
