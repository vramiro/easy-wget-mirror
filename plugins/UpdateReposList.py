#!/usr/bin/python
import os, httplib
from MirrorPlugin import MirrorPlugin
from urlparse import urlparse

class UpdateReposListException(Exception): pass

class UpdateReposList(MirrorPlugin):

	def __init__(self, *args, **kwargs):
		try:
			m = kwargs['mirror']
			super(UpdateReposList, self).__init__(m)
			config = kwargs['config']			
			self.repos_file = self.mirror.repos_file
			repos_list = config.get(UpdateReposList.__name__,'update.repos.list').split(',')
			# [file=>url,?]+
			self.update_repos_list = map(lambda entry:
						     (lambda e: (e[0], e[1]))(entry.split('=>')),
						     repos_list)			
		except Exception as e:
			raise UpdateReposListException("Unable to init UpdateReposList plugin: " + str(e))
		
	def __before__(self, buff):		
		for (repo_name, url) in self.update_repos_list:
			if self.mirror.name == repo_name:
				url_obj = urlparse(url)
				conn = httplib.HTTPConnection(url_obj.netloc)
				conn.request('GET', url_obj.path)
				response = conn.getresponse()
				if response.status == 200:
					repo_file = open(self.mirror.repos_file, 'w')
					repo_file.write(response.read())

	def __after__(self, buff):
		pass
