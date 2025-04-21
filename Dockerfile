FROM nginx:1.27-bookworm

RUN apt update && apt install -y python3 python3-pip supervisor

COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf

RUN rm -rf /usr/share/nginx/html/*
COPY . /usr/share/nginx/html/

EXPOSE 80

CMD ["supervisord", "-n"]