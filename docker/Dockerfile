FROM python:3.10-slim

LABEL maintainer="Sachin duhan <duhan.sachin126@gmail.com>"

ENV environment=production
ENV APP_PATH=/usr/src/app 
ENV user=root

RUN mkdir -p $APP_PATH \
    mkdir -p $LOG_PATH

WORKDIR $APP_PATH

COPY .. ${APP_PATH}/

# setup supervisord
RUN mkdir -p /var/log/supervisord/
RUN mkdir -p /var/log/gunicorn/

EXPOSE 5000

# Run installation scripts
RUN apt-get update && \
    apt-get install -y supervisor && \
    python3 -m pip install -r ${APP_PATH}/requirements.txt

# Create the log file to be able to run tail
RUN touch ${APP_PATH}/server.log

# add this line to make supervisor include *.ini config file from /etc/supervisor/conf.d/
RUN echo "files = /etc/supervisor/conf.d/*.ini" >> /etc/supervisor/supervisord.conf
ADD ../cronzimus-supervisord.ini /etc/supervisor/conf.d/

CMD  supervisord --nodaemon -c /etc/supervisor/supervisord.conf & tail -f ${APP_PATH}/server.log
