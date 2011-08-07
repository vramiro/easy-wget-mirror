#!/usr/bin/python

import sys, time, os
from ConfigParser import ConfigParser
from mirror import *
from utils import debug

#########
## main
def usage(script_name):
	print "%s <config file>" % (script_name)
	sys.exit(-1)

if __name__ == '__main__':
	if len(sys.argv) != 2:
		usage(sys.argv[0])

	# read config file
	config_file = open(sys.argv[1])
	config = ConfigParser()	
	config.readfp(config_file)
	conf_dir = os.path.dirname(os.path.abspath(config_file.name))

	# get default values
	wget_path = config.get('default','wget.path')
	username = config.get('default','user')
	mirrors = config.get('default','mirrors.active.list').split(';')
	plugins = config.get('default','plugins.active.list').split(';')

	for mname in mirrors:
		mirror_url = config.get(mname, 'url')
		repos_file = os.path.join(conf_dir, config.get(mname, 'repositories'))
		files_pattern= config.get(mname, 'files.pattern')
		destination_path = config.get(mname, 'destination')
		logs_path = config.get(mname, 'logs')

		m = Mirror(mname, wget_path, username, 
			   mirror_url, repos_file, files_pattern, destination_path, logs_path)

		# time run duration
		t1 = os.times()		
		m.update()
		t2 = os.times()
		rtime = t2[4] - t1[4]   # real time (including child time)

		## TODO: mode to a plugin interface
		# bw analysis
		from plugins.bandwidth import BandwidthPlugin
		bw = BandwidthPlugin(m.log_file)		
		(min, avg, max) = bw.__execute__()

		# log run-log
		runlog = open(m.log_run, 'a')
		runlog.write('Run Date:\t%s\n' % (m.run_date_str))
		runlog.write('Exec Time:\t%s secs\n' % (str(rtime)))
		runlog.write('Min bw used:\t%s KB/s\n' % (min))
		runlog.write('Avg bw used:\t%s KB/s\n' % (avg))
		runlog.write('Max bw used:\t%s KB/s\n' % (max))
		runlog.write('\n')
