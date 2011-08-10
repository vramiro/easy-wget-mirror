import os
from subprocess import Popen
from datetime import datetime

class Mirror(object):
	def __init__(self, mirror_name, wget_path, mirror_url, repos_file,
		     accept_list, destination_path, logs_path):
		try:
			self.name = mirror_name
			self.wget = wget_path
			self.mirror_url = mirror_url
                        self.repos_file = repos_file
			self.accept_list = accept_list
			self.destination = destination_path
                        self.repos_file = repos_file
                        self.logs_path = logs_path
			self.run_date = datetime.today()
			self.log_file = os.path.join(logs_path, self.name + "-" + self.run_date.strftime('%Y%m%d'))
			self.log_run = os.path.join(logs_path, self.name + "-runlog")

			self.command_format = '%s --continue --no-clobber --no-host-directories --no-parent --recursive --no-verbose --accept %s --directory-prefix=%s %s/%s --append-output=%s'			
		except Exception as e:
			raise MirrorInitException("Cannot create mirror object: " + str(e))
	
	def update(self):
		try:
			f = open(self.repos_file)
			repositories = f.read().split('\n')
                     
			for repository in repositories:
				command = self.command_format % (self.wget, self.accept_list, self.destination, self.mirror_url, repository, self.log_file)
				p = Popen(command, shell=True)
				os.waitpid(p.pid, 0)
		except Exception as e:
			raise MirrorUpdateException("Cannon update mirror: " + str(e))

	def __str__(self):
		return self.name

##Exception Management
class MirrorException(Exception): pass
class MirrorInitException(MirrorException): pass
class MirrorUpdateException(MirrorException): pass
		
