import os
from subprocess import Popen
from pwd import getpwnam
from datetime import datetime
from utils import create_dir, debug

class Mirror:

	def __init__(self, mirror_name, wget_path, username,
			   mirror_url, repos_file, accept_list, destination_path, logs_path):

		self.command_format = '%s --continue --no-clobber --no-host-directories --no-parent --recursive --no-verbose --accept %s --directory-prefix=%s %s/%s --append-output=%s'
		self.name = mirror_name
		self.wget = wget_path

		user = getpwnam(username)
		self.uid = user.pw_uid
		self.gid = user.pw_gid
		self.mirror_url = mirror_url

		f = open(repos_file)
		self.repositories = f.read().split('\n')
		self.accept_list = accept_list
		self.destination = destination_path

		# logs file
		d = datetime.today()
		self.log_date_str = d.strftime('%Y%m%d')
		self.run_date_str = d.strftime('%Y/%m/%d')
		self.log_file = os.path.join(logs_path, self.name + "-" + self.log_date_str)
		self.log_run = os.path.join(logs_path, self.name + "-runlog")

		create_dir(destination_path)
		create_dir(logs_path)

	def update(self):
		for repository in self.repositories:
			command = self.command_format % (self.wget, self.accept_list, self.destination, self.mirror_url, repository, self.log_file)
			p = Popen(command, shell=True)
			os.waitpid(p.pid, 0)
					
		for d in os.listdir(self.destination):
			path = os.path.join(self.destination, d)
			if d.startswith("@"): os.rmdir(path)

		path = self.destination
		for root, dirs, files in os.walk(path):
			for momo in dirs:
				os.chown(os.path.join(root, momo), self.uid, self.gid)
			for momo in files:
				os.chown(os.path.join(root, momo), self.uid, self.gid)

	def __str__(self):
		return self.name

##Exception Management
# TODO: raise some exceptions
class MirrorException(Exception):
	pass
class MirrorInitException(MirrorException):
	pass
class MirrorUpdateException(MirrorException):
	pass



		
