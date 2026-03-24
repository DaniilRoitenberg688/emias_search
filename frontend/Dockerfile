# 1. Этап сборки (build stage)
FROM node:18-alpine AS build

# Создадим рабочую директорию
WORKDIR /app

# Скопируем package*.json, установим зависимости
COPY package*.json .
RUN npm install


# Скопируем всё остальное и соберём проект
COPY . .
ENV NODE_ENV=production
ENV VITE_SESSION_TIME_IN_MILLISECONDS=3600000
#ENV VITE_LOGIN_API_URL='http://j-auth-ppak.vmeda.local/api/v2/login'
ENV VITE_API_URL='/api'
RUN npm run build

# 2. Этап запуска (release stage)
FROM nginx:alpine

RUN apk add --no-cache gettext

RUN mkdir static

COPY nginx.conf /etc/nginx/conf.d/default.conf

COPY --from=build /app/dist /usr/share/nginx/html

EXPOSE 8080

CMD ["/bin/sh", "-c", "envsubst < /usr/share/nginx/html/env.js.template > /usr/share/nginx/html/env.js && nginx -g 'daemon off;'"]