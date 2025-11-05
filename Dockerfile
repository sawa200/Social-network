# Базовий Python (3.13 ок, можна 3.12-slim, якщо треба стабільніші колеса)
FROM python:3.13-slim

# Не пишемо .pyc і показуємо логи відразу
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /code

# Системні пакети: компіляція та клієнт postgres (для pg_isready)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    postgresql-client \
    git \
    && rm -rf /var/lib/apt/lists/*

# Спочатку залежності — для кешу
COPY requirements.txt /code/requirements.txt
RUN pip install --upgrade pip && pip install -r requirements.txt

# Далі код
COPY . /code/

# Вхідна точка (чекаємо БД перед міграціями)
COPY docker-entrypoint.sh /docker-entrypoint.sh
RUN chmod +x /docker-entrypoint.sh

EXPOSE 8000
ENTRYPOINT ["/docker-entrypoint.sh"]
