# Imagen base de Python
FROM python:3.10

# Establecer el directorio de trabajo
WORKDIR /app

# Copiar los archivos de la aplicación
COPY requirements.txt ./
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Exponer el puerto para Flask
EXPOSE 5000

# Comando para ejecutar el servidor
CMD ["flask --app", "main", "recreate_db"]
CMD ["python", "main.py"]
