# Базовый образ с Python
FROM python:3.10
WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Запуск FastAPI-сервера через Uvicorn
CMD ["uvicorn", "Task1:app", "--host", "0.0.0.0", "--port", "8000"]