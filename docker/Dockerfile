FROM python:3.8

RUN apt-get update && apt-get -y install cron vim

# setup source code
RUN mkdir -p /app/logs
COPY ./src /app/src
RUN pip install -r ./src/requirements.txt

# setup cronjob
COPY docker/set_crontab.sh /app
RUN chmod +x /app/set_crontab.sh
RUN /app/set_crontab.sh

WORKDIR /app

# run crond as main process of container
CMD ["cron", "-f"]
