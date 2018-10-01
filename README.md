# tips
* use mysql 5.7

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
* docker pull sflyr/sqlplus

# On Mac
* Log: https://docs.docker.com/docker-for-mac/troubleshoot/#check-the-logs
* Login to VM in Hyperkit: https://stackoverflow.com/questions/39739560/how-to-access-the-vm-created-by-dockers-hyperki
* `screen ~/Library/Containers/com.docker.docker/Data/vms/0/tty` Then you can see the docker daemon

# Oralce
* Check instance name:
```sql
SELECT sys_context('USERENV','DB_NAME') AS Instance FROM dual;
select sys_context( 'userenv', 'current_schema' ) from dual;
describe employee_history;
```
* SQLPlus: `/sqlplus system/oracle@172.17.02:1521/XE

# docker network
* By default, the docker containers are connected to the same switch. You can check the ip address use command like 'ifconifg' or 'ip addr' and ping each other. The local IP address is with prefix 172.

# Docker process mapping
* On MAC, after login LinuxKit
* Got below processes structure. I started sleep in a container. The ouput of pstree isn't complete. I have to use serveral times to got my sleep process in my container.
```
linuxkit-025000000001:~# pstree -p 976
containerd(976)-+-containerd-shim(993)---acpid(1012)
                |-containerd-shim(1042)---diagnosticsd(1062)
                |-containerd-shim(1096)-+-docker-init(1114)---entrypoint.sh(113+
                |                       |-rpc.statd(1187)
                |                       |-rpcbind(1157)
                |                       `-transfused.sh(1210)---transfused(1212+
                |-containerd-shim(1161)---host-timesync-d(1180)
                |-containerd-shim(1266)---kmsg(1294)
                |-containerd-shim(1334)---sntpc(1362)
                |-containerd-shim(1595)---trim-after-dele(1657)
                |-containerd-shim(1885)---vpnkit-forwarde(1947)
                |-containerd-shim(2149)---vsudd(2181)
                `-containerd-shim(2225)---logwrite(2243)
linuxkit-025000000001:~# pstree -p 1114
docker-init(1114)---entrypoint.sh(1139)-+-logwrite(1192)---lifecycle-serve(1205+
                                        `-start-docker.sh(1190)---dockerd(1301)+
linuxkit-025000000001:~# pstree -p 1190
start-docker.sh(1190)---dockerd(1301)---docker-containe(1351)---docker-containe+
linuxkit-025000000001:~# pstree -p 1351
docker-containe(1351)---docker-containe(2315)---bash(2339)---sleep(2469)
```
* pid namespace tools:
  * https://lwn.net/Articles/259217/ : One of the new features in the upcoming 2.6.24 kernel will be the PID namespaces support developed by the OpenVZ team with the help of IBM.
  * http://hustcat.github.io/pid-namespace-and-init/
  * https://andrestc.com/post/cgroups-io/
  * http://man7.org/linux/man-pages/man7/namespaces.7.html
  * https://stackoverflow.com/questions/23513045/how-to-check-if-a-process-is-running-inside-docker-container
  * Linux Command Tools
    * `lsns'
    * `ls -l /proc/<pid>/ns`

# Docker storage mapping

# Docker CPU/Memory/Storage resource isolation
