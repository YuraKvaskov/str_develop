# Stage 1: Получаем скомпилированные файлы фронтенда
FROM annakharatova/partners-map:latest as frontend

# Stage 2: Создаем образ Nginx и копируем файлы фронтенда
FROM nginx:1.21.3-alpine

# Копируем конфигурационный файл Nginx
COPY ./nginx/default.conf /etc/nginx/conf.d/default.conf

# Копируем скомпилированные файлы фронтенда в директорию Nginx
COPY --from=frontend /app/dist /usr/share/nginx/html
