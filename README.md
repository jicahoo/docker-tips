# docker-tips

```
docker build -t imag_name .
docker run -i -t imag_name  /bin/bash
docker run -dit  python    # Docker will exit when main process ends. https://stackoverflow.com/questions/28212380/why-docker-container-exits-immediately
docker exec -ti container_name /bin/bash
sudo docker run -dti -p 80:8000 abc  #80 is host port, 8000 is container port
docker run -d -p 49161:1521 -e ORACLE_ALLOW_REMOTE=true wnameless/oracle-xe-11g
```

# docker
* https://hub.docker.com/r/wnameless/oracle-xe-11g/   (16.04)

# On Mac
* Log: https://docs.docker.com/docker-for-mac/troubleshoot/#check-the-logs

# Oralce
* Check instance name:
```sql
SELECT sys_context('USERENV','DB_NAME') AS Instance FROM dual;

```
* SQLPlus: `/sqlplus system/oracle@172.17.02:1521/XE

# docker network
* By default, the docker containers are connected to the same switch. You can check the ip address use command like 'ifconifg' or 'ip addr' and ping each other. The local IP address is with prefix 172.
