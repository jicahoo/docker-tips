# Table of contents
1. [Docker Network](#docker-network)
2. [Docker Storage](#docker-storage)
3. [Linux Namespace](#linux-namespace)
5. [Skills I learned](#new-skills)
    1. [pstree tool](#pstree-tool)
6. [FAQ](#faq)

# FAQ <a name="faq"/>
* How to enter a Docker?
    * `sudo nsenter --target <docker_pid> --mount --uts --ipc --net --pid`
* How to get docker pid? `sudo docker inspect -f {{.State.Pid}} <docker_id>`
* How to get detailed info of docker? `docker inspect <dokcer_id>`

# tips
* use mysql 5.7

# docker-tips

```
docker build -t imag_name .
docker run -i -t imag_name  /bin/bash
docker run -dit  python    # Docker will exit when main process ends. https://stackoverflow.com/questions/28212380/why-docker-container-exits-immediately
docker exec -ti container_name /bin/bash
sudo docker run -dti -p 80:8000 abc  #80 is host port, 8000 is container port
```

# docker
* https://hub.docker.com/r/wnameless/oracle-xe-11g/   (16.04)
* docker pull sflyr/sqlplus
# Virtualization
* Virtualize the hardwares: CPU, RAM, Ethernet, Disk/Filesystem?
# Install docker on Ubuntu
* wget https://download.docker.com/linux/ubuntu/dists/xenial/pool/stable/amd64/docker-ce_18.06.1~ce~3-0~ubuntu_amd64.deb
* sudo dpkg -i /path/to/package.deb
* sudo docker run hello-world

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

# docker network <a name="docker-network"></a>
* https://tonybai.com/2017/01/11/understanding-linux-network-namespace-for-docker-network/
* https://github.com/docker/libnetwork/blob/master/docs/design.md
* By default, the docker containers are connected to the same switch. You can check the ip address use command like 'ifconifg' or 'ip addr' and ping each other. The local IP address is with prefix 172.
* Virtulize ethernet adapter, separate ip route mechanism, Linux Bridge.
* https://platform9.com/blog/container-namespaces-deep-dive-container-networking/
* ![DockerNetwork](https://platform9.com/wp-content/uploads/2017/01/container_namespaces.png)

## Network tools
* Check Linux bridges:

```shell
jack@jack-virtual-machine:~$ brctl show
bridge name	bridge id		STP enabled	interfaces
docker0		8000.0242b42c694e	no		veth68c6a5d
							vethd28f675

```

* Check veth pair:
	* https://stackoverflow.com/questions/21724225/docker-how-to-get-veth-bridge-interface-pair-easily
	
```bash
function veth_interface_for_container() {
  # Get the process ID for the container named ${1}:
  local pid=$(docker inspect -f '{{.State.Pid}}' "${1}")

  # Make the container's network namespace available to the ip-netns command:
  mkdir -p /var/run/netns
  ln -sf /proc/$pid/ns/net "/var/run/netns/${1}"

  # Get the interface index of the container's eth0:
  local index=$(ip netns exec "${1}" ip link show eth0 | head -n1 | sed s/:.*//)
  # Increment the index to determine the veth index, which we assume is
  # always one greater than the container's index:
  let index=index+1

  # Write the name of the veth interface to stdout:
  ip link show | grep "^${index}:" | sed "s/${index}: \(.*\):.*/\1/"

  # Clean up the netns symlink, since we don't need it anymore
  rm -f "/var/run/netns/${1}"
}
```
	* `ethtool -S <interface>`

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
    * `ls -l /proc/<pid>/ns` In both Host & container, you can check namespace info of a given process.
    *  `cat /proc/2488/status|grep NS` . On Host, you can get the pid mapping between container pid and host pid.

# Docker storage <a name="docker-storage"/>
* 典型容器存储项目揭密：Flocker，Portworx和VSAN: http://chuansong.me/n/903169052258
* 容器应用千变万化，存储架构不离其宗: http://chuansong.me/n/484843052451
* Dell EMC slides: https://www.snia.org/sites/default/files/SDCIndia/2018/Slides/4%20-%20Dell%20EMC%20-%20Persistent%20storage%20for%20Containers.pdf

## CSI
* CSI: https://arslan.io/2018/06/21/how-to-write-a-container-storage-interface-csi-plugin/
* https://thenewstack.io/3-reasons-container-storage-interface-big-deal/
* https://kubernetes.io/blog/2018/01/introducing-container-storage-interface/
* https://github.com/container-storage-interface/spec
* Similar projects:
    * https://thecodeteam.com/projects/docker-volume-vmax/
    * https://thecodeteam.com/projects/gocsi/
    * https://thecodeteam.com/projects/csi-scaleio/
    * https://thecodeteam.com/all-projects/?fwp_per_page=90

# Docker CPU/Memory/Storage resource isolation

# Linux Namespace <a name="linux-namespace"/>
* `nsenter -t <pid> -n ip addr` . Enter the network namespace of process with pid.

# Kubernetes

## Kubernetes setup
* Successfully setup: https://github.com/pires/kubernetes-vagrant-coreos-cluster
* http://www.openwriteup.com/setting-up-kubernetes-cluster-in-vmware-workstation-vm/
* https://blogs.vmware.com/cloudnative/2017/10/25/kubernetes-introduction-vmware-users/
* https://blog.inkubate.io/install-and-manage-automatically-a-kubernetes-cluster-on-vmware-vsphere-with-terraform-and-kubespray/
* http://www.joseluisgomez.com/containers/kubernetes-deployment/

## Kubernetes usage
* https://kubernetes.io/docs/reference/kubectl/cheatsheet/#interacting-with-nodes-and-cluster
* https://kubernetes.io/docs/tasks/run-application/run-stateless-application-deployment/
* Get detailed info of POD: `kubectl describe pod source-ip-app-8687dbf9f-r9gxx`
* Check the network namespace via a hack way: https://thenewstack.io/hackers-guide-kubernetes-networking/

## Kubernetes distrituions
* https://dzone.com/articles/kubernetes-distributions-how-do-i-choose-one

## CSI

* https://kubernetes-csi.github.io/docs/Example.html
* http://www.itdks.com/dakashuo/13698/material/2644/download OpenSDS Huawei CSI

## Deploy a nginx to k8s
* `kubectl create deployment nginx --image=nginx`
* `kubectl describe deployment nginx`
* `kubectl create service nodeport nginx --tcp=80:80`
* `kubectl get svc`
```bash
NAME         TYPE        CLUSTER-IP     EXTERNAL-IP   PORT(S)        AGE
kubernetes   ClusterIP   10.100.0.1     <none>        443/TCP        2h
nginx        NodePort    10.100.52.54   <none>        80:32177/TCP   47m
```
* Access from non-master node: http://master-ip:32177. You will see nginx.



# Skills I learned <a name="new-skills"/>
## Check process <a name="pstree-tool"/>
* `pstree -spa <pid>` Get the pid's ancestors.

## TOC of Markdown
* https://stackoverflow.com/questions/11948245/markdown-to-create-pages-and-table-of-contents

## Network namespace not visible
* https://stackoverflow.com/questions/31265993/docker-networking-namespace-not-visible-in-ip-netns-list
