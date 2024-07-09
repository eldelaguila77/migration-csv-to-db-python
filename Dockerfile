FROM python:3.8

# Instala cron y cualquier otra dependencia necesaria
RUN apt-get update && apt-get install -y cron && rm -rf /var/lib/apt/lists/*
RUN chmod 0644 /etc/cron.d/
#RUN /usr/bin/crontab /etc/cron.d/crontab

# Crea un directorio para tu aplicación
WORKDIR /app


# Opcional: Copia tu código Python al contenedor, si quieres tener una copia base en la imagen
COPY . /app

# Opcional: Instala las dependencias de tu proyecto Python
RUN pip install --no-cache-dir -r /app/app/requirements.txt
RUN chmod 0644 crontab
RUN crontab crontab
RUN touch /var/log/cron.log

# Da permiso de ejecución al script principal, si es necesario
# RUN chmod +x /app/main.py

# Comando para iniciar cron y tu aplicación
CMD ["sh", "-c", "cron && tail -f /var/log/cron.log"]
#CMD ["sh", "-c", "cron && python /app/main.py"]