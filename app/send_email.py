import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
import os
import configparser

# Leer configuración
config = configparser.ConfigParser()
config.read('/config/config.ini')

def send_email_with_attachment(email, subject_base, body, file_path):
    # Leer el contenido del archivo de log una sola vez
    if os.path.exists(file_path):
        with open(file_path, "rb") as attachment:
            file_content = attachment.read()
    
        # Determinar si hay errores en el log
        if "Error" in file_content.decode() or "Exception" in file_content.decode() or "ERROR" in file_content.decode() or "Failed" in file_content.decode():
            subject = f"{subject_base} - Errores Encontrados"
        elif "Warning" in file_content.decode() or "WARNING" in file_content.decode() or "Warn" in file_content.decode() or "Advertencia" in file_content.decode():
            subject = f"{subject_base} - Advertencias Encontradas"
        else:
            subject = f"{subject_base} - Proceso Finalizado Exitosamente"
    else:
        # Si el archivo no existe, ajustar el asunto y el cuerpo del mensaje adecuadamente
        subject = f"{subject_base} - Archivo No Encontrado"
        body = "El archivo especificado no fue encontrado."
        file_content = None

    # Configuración del correo
    sender_email = config['email']['from']
    sender_password = config['email']['sender_password']
    receiver_email = email

    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = subject
    message.attach(MIMEText(body, "html"))

    # Adjuntar el archivo si existe
    if file_content:
        part = MIMEApplication(file_content, Name=os.path.basename(file_path))
        part['Content-Disposition'] = f'attachment; filename="{os.path.basename(file_path)}"'
        message.attach(part)

    # Convert message to string
    text = message.as_string()

    # Send email
    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, receiver_email, text)
        print("Email sent successfully")