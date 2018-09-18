# docker-tips

```
docker build -t imag_name .
docker run -i -t imag_name  /bin/bash
docker run -dit  python    # Docker will exit when main process ends. https://stackoverflow.com/questions/28212380/why-docker-container-exits-immediately
docker exec -ti container_name /bin/bash
sudo docker run -dti -p 80:8000 abc  #80 is host port, 8000 is container port.
```

# docker
* https://hub.docker.com/r/wnameless/oracle-xe-11g/   (16.04)

# On Mac
* Log: https://docs.docker.com/docker-for-mac/troubleshoot/#check-the-logs
