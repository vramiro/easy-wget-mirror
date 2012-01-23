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

				# TODO: improve this in a factory method?
				if url.endswith(".txt"):
					handler = UpdateFromTextList(data)
				elif url.endswith(".xml.gz"):
					handler = UpdateFromSiteMap(data)
				else: 
					raise UpdateReposListException("Unable to handle data type: " + url)

				handled_data = handler.handle()
				repo_file = open(self.mirror.repos_file, 'w')
				repo_file.write(handled_data)
				repo_file.close()


	def __after__(self, buff):
		pass


class UpdateFrom:
	def __init__(self, data):
		self.data = data

class UpdateFromTextList(UpdateFrom):
	def __handle__(self):
		return self.data

import xml.dom.minidom, tempfile, subprocess, re

class UpdateFromSiteMap(UpdateFrom):
		
	class SiteMapXMLTraverser:
		def __init__(self, xmlStr):
			self.doc = xml.dom.minidom.parseString(xmlStr)

		def getContents(self):
			buff = []
			m = re.compile('http:\/\/(.*)\/(\w+)\/?')
			urlSet = self.doc.getElementsByTagName("urlset")[0]
			for urlNode in urlSet.getElementsByTagName("url"):
				url = self.getText(urlNode.getElementsByTagName("loc")[0].childNodes)
				res = m.match(url)
				if None != res: buff.append(res.group(2)) 
			buff.sort()
			return buff

		def getText(self, nodelist):
			rc = []
			for node in nodelist:
				if node.nodeType == node.TEXT_NODE:
					rc.append(node.data)
			return ''.join(rc)

	def handle(self):
		(f, tmpname) = tempfile.mkstemp()
		os.write(f,self.data)
		os.close(f)
		uncompressed_buffer = subprocess.Popen(['gzcat', tmpname], stdout=subprocess.PIPE).communicate()[0]
		xmlTraverser = UpdateFromSiteMap.SiteMapXMLTraverser(uncompressed_buffer)
		repos = xmlTraverser.getContents()
		print repos
		os.unlink(tmpname)
		return '\n'.join(repos)

