# Usa una imagen base oficial de Python
FROM python:3.12-slim
WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8500

ENTRYPOINT ["streamlit", "run", "app.py"]

## Comandos para construir y ejecutar la imagen
# docker build --no-cache -t todo-app .
# docker run --rm -p 8500:8501 -v dumped:/app/dumped --name c_todo-app todo-app
