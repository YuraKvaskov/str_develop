FROM python:3.11-slim

# Установка зависимостей системы
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Установка рабочего каталога
WORKDIR /app

# Копирование файлов зависимостей
COPY backend/requirements.txt ./

# Установка зависимостей Python
RUN pip install --no-cache-dir -r requirements.txt

# Копирование исходного кода приложения
COPY backend/ .

RUN python manage.py migrate
RUN python manage.py collectstatic --noinput

# Открытие порта для Gunicorn
EXPOSE 8000

# Команда запуска приложения
CMD ["gunicorn", "StrProject.wsgi:application", "--bind", "0.0.0.0:8000"]
