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
			self.update_repos_list = {}
			for entry in repos_list:
				e = entry.split('=>')
				self.update_repos_list[e[0]] = e[1]
		except Exception as e:
			raise UpdateReposListException("Unable to init UpdateReposList plugin: " + str(e))
		
	def __before__(self, buff):
		if self.mirror.name in self.update_repos_list:
			(repo_name, url) = (self.mirror.name, self.update_repos_list[self.mirror.name])
			url_obj = urlparse(url)
			conn = httplib.HTTPConnection(url_obj.netloc)
			conn.request('GET', url_obj.path)
			response = conn.getresponse()
			if response.status == 200:

				data = response.read()
				handler = None
				if url.endswith(".txt"):
					handler = UpdateFromTextHandler(data)
				elif url.endswith(".xml.gz"):
					handler = UpdateFromSiteMapHandler(data)
					
				handled_data = handler.handle()
				repo_file = open(self.mirror.repos_file, 'w')
				repo_file.write(handled_data)

	def __after__(self, buff):
		pass


class UpdateFrom:
	def __init__(self, data):
		self.data = data

class UpdateFromTextList(UpdateFrom):
	def __handle__(self):
		return self.data

class UpdateFromSiteMap(UpdateFrom):
	import zlib, xml.dom.minidom

	def handle(self):
		uncompressed_buffer = zlib.decompress(self.data)
		xmlTraverser = SiteMapXMLTraverser(uncompressed_buffer)
		return xmlTraverser.getContents()
		
	class SiteMapXMLTraverser:
		def __init__(self, xml):		
			self.doc = xml.dom.minidom.parseString(xml)

		def getContents(self):
			buff = ""
			urlSet = doc.getElementsByTagName("urlset")
			for urlNode in urlSet.getElementsByTagName("url"):
				url = getText(urlNode.getElementsByTagName("loc")[0].data)
				buff.append(url)
			return buff


