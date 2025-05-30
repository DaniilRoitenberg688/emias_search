# Базовый образ
FROM python:3.13-slim

# Установи рабочую директорию
WORKDIR /app

# Скопируй зависимости и установи их
RUN pip install --no-cache-dir --upgrade pip
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Скопируй весь код
COPY . .

# Открой порт 5000
EXPOSE 8000

# Запусти Gunicorn
CMD ["uvicorn", "app:app", "--port", "8000", "--host", "0.0.0.0"]
