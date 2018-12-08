import os
import time
import json
import subprocess
from StringIO import StringIO
from decimal import Decimal
import optparse
class DockerMonitoring:
	__inputJSON=""
	__outputJSON=""
	__dockerContainerId=""
	def __init__(self):
		self.__inputJSON=""
		self.__outputJSON=""
		self.__containerId=""
	def discoverContainers(self):
		try:
			output = subprocess.check_output("curl --silent  --unix-socket /var/run/docker.sock http:/containers/json", shell=True)
			io = StringIO(output)
			self.__inputJSON=json.load(io)
			first = True
			items=""
			for record in self.__inputJSON:
				if first:
					item="{\"{#CONTAINERNAMES}\":\""+str(record['Names'][0]).replace('/', '')+"\",\"{#CONTAINERIDS}\": \""+str(record['Id'])+"\"}"
					first = False
				else:
					item=",{\"{#CONTAINERNAMES}\":\""+str(record['Names'][0]).replace('/', '')+"\",\"{#CONTAINERIDS}\": \""+str(record['Id'])+"\"}"
				items=items+item
			self.__outputJSON="{\"data\":["+str(items)+"]}"
			return self.__outputJSON
		except Exception as e:
			return "-1"
	def containerAvailability(self,dockerContainerId):
		try:
			if(os.path.exists("/sys/fs/cgroup/cpu/docker/"+str(dockerContainerId))):
				return subprocess.check_output("ps -ef | grep -w \"docker-containerd-shim "+str(dockerContainerId)+"\" | wc -l | awk '{if($1 >= 3) {printf 1;} else {printf 0;}}'", shell=True)
			else:
				return ""
		except Exception as e:
			return "-1"

	def containerUtilCpuPercentage(self,dockerContainerId):
		try:
			clockTicksPerSecond=int(os.sysconf(os.sysconf_names['SC_CLK_TCK']))
			nanoSecondsPerSecond=1000000000
			if(self.containerAvailability(dockerContainerId)=="1"):
				interval = 1
				previousCpuUsage = Decimal(subprocess.check_output("cat /sys/fs/cgroup/cpuacct/docker/"+dockerContainerId+"/cpuacct.usage", shell=True))
				previousSystemUsage = Decimal(subprocess.check_output("cat /proc/stat|grep -w cpu|awk '{split($0,a,\" \"); sum=0; for(i=2;i<8;i++)(sum+=a[i])} END{print sum }'", shell=True))*(nanoSecondsPerSecond/clockTicksPerSecond)
				time.sleep(interval)
				currentCpuUsage = Decimal(subprocess.check_output("cat /sys/fs/cgroup/cpuacct/docker/"+dockerContainerId+"/cpuacct.usage", shell=True))
				currentSystemUsage = Decimal(subprocess.check_output("cat /proc/stat|grep -w cpu|awk '{split($0,a,\" \"); sum=0; for(i=2;i<8;i++)(sum+=a[i])} END{print sum }'", shell=True))*(nanoSecondsPerSecond/clockTicksPerSecond)
				totalCpuCore = int(subprocess.check_output("cat /sys/fs/cgroup/cpuacct/docker/"+dockerContainerId+"/cpuacct.usage_percpu| awk '{n=split($0, array,\" \")} END{print n }'", shell=True))
				cpuDelta = currentCpuUsage - previousCpuUsage
				systemDelta = currentSystemUsage - previousSystemUsage
				cpuPercent = 0
				if(systemDelta > 0 and cpuDelta > 0):
					cpuPercent = float("{0:.2f}".format(Decimal(cpuDelta / systemDelta) * totalCpuCore * 100))
				return cpuPercent
			else:
				return ""
		except Exception as e:
			return "-1"
	def containerUtilMemoryPercentage(self,dockerContainerId):
		try:
			if(self.containerAvailability(dockerContainerId)=="1"):
				memoryUsage = Decimal(long(subprocess.check_output("cat /sys/fs/cgroup/memory/docker/"+dockerContainerId+"/memory.usage_in_bytes", shell=True))/(1024))
				memoryCache = Decimal(long(subprocess.check_output("cat /sys/fs/cgroup/memory/docker/"+dockerContainerId+"/memory.stat | grep -i cache | head -n 1 | awk '{ print $2 }'", shell=True))/(1024))
				memoryUsage = memoryUsage - memoryCache
				memoryLimit = Decimal(long(subprocess.check_output("cat /sys/fs/cgroup/memory/docker/"+dockerContainerId+"/memory.limit_in_bytes", shell=True))/(1024))
				hostMemoryLimit = Decimal(subprocess.check_output("cat /proc/meminfo|grep -w MemTotal|awk '{split($0,a,\" \"); printf a[2]}'", shell=True))
				if(memoryLimit > hostMemoryLimit):
					memoryLimit = hostMemoryLimit
				memoryPercent = 0
				if(memoryUsage > 0 and memoryLimit > 0):
					memoryPercent = Decimal(memoryUsage / memoryLimit) * 100
				return float(str(round(memoryPercent, 2)));
			else:
				return ""
		except Exception as e:
			return "-1"
	def containerUtilMemoryUsage(self,dockerContainerId,metric):
		try:
			if(self.containerAvailability(dockerContainerId)=="1"):
				output = subprocess.check_output("cat /sys/fs/cgroup/memory/docker/"+dockerContainerId+"/memory.stat|grep -w "+metric+"|awk '{split($0,a,\" \"); printf a[2]}'", shell=True)
				return output;
			else:
				return ""
		except Exception as e:
			return "-1"

def main():
	obj = DockerMonitoring()
	parser = optparse.OptionParser()
	parser.add_option('--metric', help='Specify the required metric to output')
	parser.add_option('--cid', help='Specify the ID of container')
	(options, args) = parser.parse_args()
	if not options.metric:
		parser.error('At least one metric should be specified')
	elif(options.metric == 'discovery'):
		print(str(obj.discoverContainers()))
	elif options.metric == 'availability':
		if not options.cid:
			parser.error('Container Id should be specified')
		else:
			print(str(obj.containerAvailability(options.cid)))
	elif options.metric == 'cpu_usage':
		if not options.cid:
			parser.error('Container Id should be specified')
		else:
			print(str(obj.containerUtilCpuPercentage(str(options.cid))))
	elif options.metric == 'mem_usage':
		if not options.cid:
			parser.error('Container Id should be specified')
		else:
			print(str(obj.containerUtilMemoryPercentage(str(options.cid))))
	elif options.metric == 'total_cache':
		if not options.cid:
			parser.error('Container Id should be specified')
		else:
			print(str(obj.containerUtilMemoryUsage(str(options.cid),"total_cache")))
	elif options.metric == 'total_swap':
		if not options.cid:
			parser.error('Container Id should be specified')
		else:
			print(str(obj.containerUtilMemoryUsage(str(options.cid),"total_swap")))
	elif options.metric == 'total_rss':
		if not options.cid:
			parser.error('Container Id should be specified')
		else:
			print(str(obj.containerUtilMemoryUsage(str(options.cid),"total_rss")))
	elif options.metric == 'total_pgfault':
		if not options.cid:
			parser.error('Container Id should be specified')
		else:
			print(str(obj.containerUtilMemoryUsage(str(options.cid),"total_pgfault")))
	else:
		parser.error('Invalid Metric')

if __name__ == "__main__":
	main()
