FROM tiangolo/uwsgi-nginx-flask:python3.6-alpine3.7

ENV STATIC_URL /static
ENV STATIC_PATH /var/www/app/static

COPY ./requirements.txt /var/www/requirements.txt

COPY . /app
RUN pip install -r /var/www/requirements.txt

EXPOSE 8080

ENTRYPOINT [ "python" ]
CMD [ "/app/server.py" ]
