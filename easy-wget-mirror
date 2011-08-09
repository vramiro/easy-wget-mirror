#!/usr/bin/python

import sys, time, os
from warnings import warn
from ConfigParser import ConfigParser
from StringIO import StringIO
from Mirror import *

APP_NAME = 'easy-wget-mirror'

def usage(script_name):
	exit("%s <config file>" % (script_name))

def load_plugins(plugin_list_name, config, mirror):
	list = []
	for pname in plugin_list_name:
		package = __import__('plugins.' + pname, fromlist=[])
		module = getattr(package, pname)
		pclass = getattr(module, pname)
		list.append(pclass(mirror=mirror,config=config))
	return list

def run(config, mirror_name, wget_path, mirror_url, repos_file, accept_list,
	destination_path, logs_path, plugin_list_name):	
	try:
		# init mirror
		m = Mirror(mirror_name, wget_path, mirror_url, repos_file,
			   accept_list, destination_path, logs_path)

		# load plugins
		try:
			plugins = load_plugins(plugin_list_name, config, m)
		except Exception as e:
			exit("Unable to load plugins: " + str(e))

		## Plugins __before__ call
		plugins_buff = StringIO()
		for plugin in plugins:
			try:
				plugin.__before__(plugins_buff)
			except Exception as e:
				warn("Failed to execute __before__ in %s with: %s" % (plugin.__class__.__name__, str(e)))

		try:
			m.update()
		except MirrorUpdateException:
			warn("Failed Update for %s. Check logs files at %s and %s" % (mirror_name, m.log_run, m.log_file))

		## Plugins __after__ call
		for plugin in plugins:
			try:
				plugin.__after__(plugins_buff)
			except Exception as e:
				warn("Failed to execute __after__ in %s with: %s" % (plugin.__class__.__name__, str(e)))

		# log run-log
		runlog = open(m.log_run, 'a')
		runlog.write(plugins_buff.getvalue())
		runlog.write('\n')
		
	except MirrorInitException as e:
		warn("Failed to create mirror: %s. No update performed" % (mirror_name))

	
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

	# get app config values
	try:
		wget_path = config.get(APP_NAME,'wget.path')
		mirrors = [x.strip() for x in
			   config.get(APP_NAME,'mirrors.active.list').split(',')]

		plugins = [x.strip() for x in
			   config.get(APP_NAME,'plugins.active.list').split(',')]
	except Exception:
		exit("Bad configuration option in: " + APP_NAME)

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

		run(config, mname, wget_path, mirror_url, repos_file,
		    files_pattern, destination_path, logs_path, plugins)
	
