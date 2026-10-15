FROM node:22-alpine AS build
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build

# Runtime: unprivileged Nginx (runs as non-root uid 101, listens on 8080)
FROM nginxinc/nginx-unprivileged:1.27-alpine
USER root
RUN apk --no-cache upgrade
USER 101
ENV BACKEND_HOST=backend:8000
COPY --from=build /app/dist /usr/share/nginx/html
COPY nginx/default.conf.template /etc/nginx/templates/default.conf.template
EXPOSE 8080
