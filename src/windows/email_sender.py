from src.async_utils import run_in_background
from src.get_credentials import credentials
from pathlib import Path
import re

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.header import Header
from email.utils import formataddr
import smtplib

patron = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"


@run_in_background
def send_email(image_paths: list[str | Path], image_description: str, email: str):
    smtp_server = "smtp.gmail.com"
    smtp_port = 465
    username = credentials.email_server_email
    password = credentials.email_server_password

    email_to_notificate = (
        email if re.match(patron, email) else credentials.email_server_send_to
    )

    msg = MIMEMultipart()
    msg["From"] = formataddr(
        (str(Header("Alerta: Matan a un amigo tuyo", "utf-8")), username)
    )
    msg["To"] = email_to_notificate
    msg["Subject"] = str(Header("⚠️ ¡Hay una amenaza! ⚠️", "utf-8"))

    email_body = f"Situación:\n\n{image_description}".encode(
        "utf-8", errors="ignore"
    ).decode("utf-8")
    msg.attach(MIMEText(email_body, "plain", "utf-8"))

    for i, image_path in enumerate(image_paths):
        try:
            with open(image_path, "rb") as image_file:
                image = MIMEImage(image_file.read())
                image.add_header(
                    "Content-Disposition", "attachment", filename=f"imagen_capturada_{i+1}.png"
                )
                msg.attach(image)
        except Exception as e:
            print(f"No se pudo adjuntar la imagen {image_path}: {e}")

    try:
        with smtplib.SMTP_SSL(smtp_server, smtp_port) as server:
            server.login(username, password)
            server.sendmail(msg["From"], msg["To"], msg.as_string())
            print("Correo enviado exitosamente.")
    except Exception as e:
        print(f"Error al enviar el correo: {e}")