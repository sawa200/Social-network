# Используем официальный Python образ
FROM python:3.13-slim

# Переменные окружения
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /code

# Системные зависимости
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    git \
    && rm -rf /var/lib/apt/lists/*

# Аргумент для Git репозитория
ARG REPO_URL=https://github.com/sawa200/Social-network.git

# Клонируем репозиторий
RUN git clone ${REPO_URL} /code

# Устанавливаем зависимости
RUN pip install --upgrade pip
COPY requirements.txt /code/
RUN pip install -r requirements.txt

# Открываем порт
EXPOSE 8000

# Команда по умолчанию
CMD ["bash", "-c", "python manage.py migrate && python manage.py createsuperuser --noinput || true && python manage.py runserver 0.0.0.0:8000"]
