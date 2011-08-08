#!/usr/bin/python

import sys, time, os
from warnings import warn
from ConfigParser import ConfigParser
from StringIO import StringIO
from mirror import *
from utils import debug
from new import instance

APP_NAME = 'easy-wget-mirror'
PLUGINS_CLS = []

def usage(script_name):
	exit("%s <config file>" % (script_name))

def load_plugins(plugins):
	for p in plugins:
		package = __import__('plugins.' + p, fromlist=[])
		module = getattr(package, p)
		pclass = getattr(module, p)
		PLUGINS_CLS.append(pclass)

def run(mname, wget_path, username, mirror_url, repos_file,
	files_pattern, destination_path, logs_path):
	try:

		m = Mirror(mname, wget_path, username, mirror_url, repos_file,
			   files_pattern, destination_path, logs_path)

		## Plugins __before__ call
		plugin_obj = []
		buff = StringIO()
		for pclass in PLUGINS_CLS:
			plugin = pclass(mirror=m)
			plugin_obj.append(plugin)
			plugin.__before__(buff)

		# time run duration
		t1 = os.times()
		try:
			m.update()
		except MirrorUpdateException:
			warn("Failed Update for %s. Check logs files at %s and %s" % (mname, m.log_run, m.log_file))

		t2 = os.times()
		rtime = t2[4] - t1[4]   # real time (including child time)

		## Plugins __after__ call
		for plugin in plugin_obj:
			plugin.__after__(buff)

		# log run-log
		runlog = open(m.log_run, 'a')
		runlog.write('Run Date:\t%s\n' % (m.run_date_str))
		runlog.write('Exec Time:\t%s secs\n' % (str(rtime)))		
		runlog.write(buff.getvalue())
		runlog.write('\n')
		
	except MirrorInitException:
		warn("Failed to create mirror: %s. No update performed" % (mname))

	
#########
## main
if __name__ == '__main__':
	if len(sys.argv) != 2:
		usage(sys.argv[0])

	# read config file
	config_file_name=sys.argv[1]		
	try:
		config_file = open(config_file_name)
		config = ConfigParser()	
		config.readfp(config_file)
		conf_dir = os.path.dirname(os.path.abspath(config_file.name))
	except Exception:
		exit("Cannot read config file: " + config_file_name)

	# get default values
	try:
		wget_path = config.get(APP_NAME,'wget.path')
		username = config.get(APP_NAME,'user')
		mirrors = config.get(APP_NAME,'mirrors.active.list').split(';')
		plugins = config.get(APP_NAME,'plugins.active.list').split(';')
	except Exception:
		exit("Bad Configuration option in: " + APP_NAME)

	load_plugins(plugins)

	for mname in mirrors:
		try:
			mirror_url = config.get(mname, 'url')
			repos_file = os.path.join(conf_dir,
						  config.get(mname, 'repositories'))
			files_pattern= config.get(mname, 'files.pattern')
			destination_path = config.get(mname, 'destination')
			logs_path = config.get(mname, 'logs')
		except Exception:
			exit("Bad configuration option for mirror: " + mname)

		run(mname, wget_path, username, mirror_url, repos_file,
		    files_pattern, destination_path, logs_path)
	
