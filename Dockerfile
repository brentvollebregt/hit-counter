FROM tiangolo/uwsgi-nginx-flask:python3.8-alpine

COPY . /app

COPY docker/.aws /root/.aws
COPY docker/sqlitebackup.sh /usr/local/bin/
COPY docker/supervisor.d/ /etc/supervisor.d/
COPY docker/prestart.sh /app/.

RUN chmod 755 /usr/local/bin/sq*

RUN apk add --no-cache bash sqlite
RUN pip3 install awscli awscli_plugin_endpoint

RUN cd /usr/local/bin && wget https://raw.githubusercontent.com/jacobtomlinson/docker-sqlite-to-s3/master/sqlite-to-s3.sh && chmod 755 sqlite*

RUN aws configure set plugins.endpoint awscli_plugin_endpoint

RUN pip install -r /app/requirements.txt
VOLUME /app/data/
