FROM python:3.8
RUN apt-get update && apt-get -y install cron vim
WORKDIR /app
RUN mkdir -p /app/logs
COPY crontab /etc/cron.d/crontab

COPY ./app/covid-19_crawler /app/covid-19_crawler

RUN pip install -r /app/covid-19_crawler/requirements.txt

RUN chmod 0644 /etc/cron.d/crontab
RUN /usr/bin/crontab /etc/cron.d/crontab

# run crond as main process of container
CMD ["cron", "-f"]
