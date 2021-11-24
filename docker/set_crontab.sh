#!/bin/sh

cat << EOF > /etc/cron.d/crontab
HOST_IP=${1}
APP_KEY=${2}
youtube_api_key=${3}
00,20,40 05-10 * * * /usr/local/bin/python3.8 /app/src/main.py video >> /app/logs/video.log 2>&1
00 16 * * * /usr/local/bin/python3.8 /app/src/main.py news >> /app/logs/news.log 2>&1
EOF

crontab /etc/cron.d/crontab

