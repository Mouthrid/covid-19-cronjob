FROM python:3.8-slim-buster

ARG HOST_IP
ARG APP_KEY
ARG YT_API_KEY

RUN apt-get update && apt-get -y install cron vim

# setup source code
RUN mkdir -p /app/logs
COPY src /app/src
RUN pip install -r /app/src/requirements.txt --no-cache-dir

# setup cronjob
COPY docker/set_crontab.sh /app
RUN chmod +x /app/set_crontab.sh
RUN /app/set_crontab.sh ${HOST_IP} ${APP_KEY} ${YT_API_KEY}

WORKDIR /app

# run crond as main process of container
CMD ["cron", "-f"]
