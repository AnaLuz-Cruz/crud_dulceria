
# Usa una imagen base de Python
FROM python:3.10-slim

# Establece el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copiar el archivo requirements.txt primero
COPY requirements.txt /app/

# Instala las dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Copia el resto de la aplicación
COPY . .

# Expone el puerto que utilizará Flask
EXPOSE 5000


# Comando para correr la aplicación
CMD ["flask","--app", "app", "run","--host=0.0.0.0"]