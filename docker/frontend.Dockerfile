FROM nginx:1.27-alpine

COPY docker/nginx/frontend.conf /etc/nginx/conf.d/default.conf
COPY auth /usr/share/nginx/html/auth
COPY css /usr/share/nginx/html/css
COPY script /usr/share/nginx/html/script
COPY assets /usr/share/nginx/html/assets
