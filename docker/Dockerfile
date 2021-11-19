FROM python:3.8

RUN apt-get update && apt-get -y install cron vim

# setup source code
RUN mkdir -p /app/logs
COPY ./src /app/src
RUN pip install -r ./src/requirements.txt

# setup cronjob
COPY docker/crontab /etc/cron.d/crontab
RUN chmod 0644 /etc/cron.d/crontab
RUN /usr/bin/crontab /etc/cron.d/crontab

WORKDIR /app

# run crond as main process of container
CMD ["cron", "-f"]
