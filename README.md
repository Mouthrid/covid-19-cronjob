# docker-python-cronjob

The cronjob for executing web crawler regularly.

```bash
$ docker-compose [COMMAND]
# start      Start services
# stop       Stop services
# up         Create and start containers
# down       Stop and remove containers, networks, images, and volumes

# RUN
$ docker-compose up --build -d
# STOP
$ docker-compose stop
# DELETE
$ docker-compose down
```

# Environment Variables

docker/crawler.env
```
APP_KEY= # backend app_key
youtube_api_key= # apply from gooel api
```
