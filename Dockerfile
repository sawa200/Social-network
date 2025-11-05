# Используем официальный образ Python
FROM python:3.13-slim

# Устанавливаем переменные окружения
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Устанавливаем рабочую директорию внутри контейнера
WORKDIR /code

# Устанавливаем системные зависимости для psycopg2 и других пакетов
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Копируем зависимости
COPY requirements.txt /code/

# Устанавливаем зависимости Python
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Копируем весь проект
COPY . /code/

# Открываем порт
EXPOSE 8000

# Команда по умолчанию (определяется в docker-compose)
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
