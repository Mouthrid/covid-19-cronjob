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

# Build image

```
docker build -f docker/Dockerfile --build-arg HOST_IP=[backend_api_ip] --build-arg APP_KEY=[backend_app_key] --build-arg YT_API_KEY=[youtube_api_key] -t covid19-cronjob-dev:latest .
```
