#!/bin/bash
python manage.py makemigrations --noinput

# Выполнение миграций
python manage.py migrate --noinput

# Сбор статических файлов
python manage.py collectstatic --noinput

# Запуск приложения
exec "$@"