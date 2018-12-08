# Zabbix-Docker_monitoring_using_CGROUPS
This project contains the steps to configure zabbix monitoring for the docker container(using linux cgroups) which are running inside docker-swarm.

# Introduction
This project focuses on configuring basic docker monitoring using zabbix-agent.The metric related with docker container which would be monitored as part of this project is mentioned below:
1. CPU utilization(%)
2. Memory utilization(%)
3. Used cache memory(Bytes)
4. Total page fault(Bytes)
5. Used RSS memory(Bytes)
6. Used swap memory(Bytes)

# Pre-requisite
Following points needs to be fulfill before starting the implementation:
- Docker container should be running inside docker-swarm on the server which needs to be monitored.
- Docker API should be enabled and accessible by running the command "curl --silent --unix-socket /var/run/docker.sock http:/containers/json".
- Docker container should be mounted on the cgroup.This could be checked running the command "ls -ltra /sys/fs/cgroup/cpu/docker/[CONTAINER-ID]".(Note:Replace "[CONTAINER-ID]" in the command with the your docker container id)
- This project was built on Python 2.7.5 hence the same Python version or any latest version compatible with Python 2.7.5 would be required.
- This project has been tested and implemented on "Red Hat Enterprise Linux Server 7.2 (Maipo)" and may not work on any other Linux distribution.

# Installation Steps:

Add the userparameter_docker.conf file in the server containing the zabbix agent under the path /etc/zabbix/zabbix_agentd.d/

# Support
 - First try to troubleshoot problems yourself. Increase debug level and check the agent logs. Try to obtain raw values from the agent.

 - Other options:
    - Try to ask Zabbix community http://www.zabbix.org/wiki/Getting_help
    - If you need support directly then send an email to mohitrajvardhan17@gmail.com for support.

All reported issues, which are not real issues, but requests for support will be closed with reference to this README section.

# License

This project is licensed under the terms of the GNU General Public License v3.0 license.
