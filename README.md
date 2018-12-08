# Zabbix-Docker_monitoring_using_CGROUPS
This project contains the steps to configure zabbix monitoring for the docker-container(using linux cgroups) which are running inside docker-swarm.

# Introduction



# Prerequisite
Following points needs to be fulfill before starting the implementation:
- 1. Docker container should be running inside socker-swarm on the server.
- 2. Docker 

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
