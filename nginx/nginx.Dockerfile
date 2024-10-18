# Этап 1: Сборка фронтенда
FROM node:20.10.0-alpine AS frontend-build
WORKDIR /app
COPY frontend/package*.json ./
RUN npm install
COPY frontend/ ./
RUN npm run build

# Этап 2: Сборка образа Nginx с фронтендом
FROM nginx:1.21.3-alpine
COPY nginx/default.conf /etc/nginx/conf.d/default.conf
COPY --from=frontend-build /app/dist /usr/share/nginx/html
# SSL сертификаты монтируются при запуске контейнера
RUN chmod -R 755 /usr/share/nginx/html
EXPOSE 80 443


### Используем базовый образ Nginx
##FROM nginx:1.21.3-alpine
##
### Копируем файл конфигурации Nginx в соответствующую директорию
##COPY ./nginx/default.conf /etc/nginx/conf.d/default.conf
##
#### Копируем скомпилированные файлы фронтенда из тома в директорию Nginx
###COPY --from=frontend /app/dist /usr/share/nginx/html
##
### Установка прав на директорию, если требуется
##RUN chmod -R 755 /usr/share/nginx/html
##
### Открываем порт 80 для внешнего доступа
##EXPOSE 80
#
#
#FROM node:20.10.0-alpine as frontend-build
#WORKDIR /app
#COPY frontend/package*.json ./
#RUN npm install
#COPY frontend/ ./
#RUN npm run build
#
## Этап 2: Сборка образа Nginx с скомпилированными файлами
#FROM nginx:1.21.3-alpine
#COPY nginx/default.conf /etc/nginx/conf.d/default.conf
#COPY --from=frontend-build /app/dist /usr/share/nginx/html
#RUN chmod -R 755 /usr/share/nginx/html
#EXPOSE 80