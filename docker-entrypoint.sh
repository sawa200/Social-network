#!/usr/bin/env bash
set -e

if [ -n "$DB_HOST" ]; then
  echo "Waiting for Postgres at $DB_HOST:$DB_PORT ..."
  until pg_isready -h "$DB_HOST" -p "$DB_PORT" -U "$POSTGRES_USER" > /dev/null 2>&1; do
    sleep 1
  done
  echo "Postgres is ready."
fi

python manage.py migrate --noinput

exec python manage.py runserver 0.0.0.0:8000
