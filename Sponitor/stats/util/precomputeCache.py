# Precompute cache

from django.core.management import setup_environ
from Sponitor import settings
setup_environ(settings)

from django.core.cache import cache
from django.test.client import Client

from mongoengine.django.auth import User

import random
import string
import logging
import json
import os

try:
	VERSIONS = json.loads(os.environ['NS2_VERSIONS'])
except:
	VERSIONS = [
		"215", 
		"213", 
		"212"
	]

try:
	MAPS = json.loads(os.environ['NS2_MAPS'])
except:
	MAPS = [
		"ns2_mineshaft", 
		"ns2_summit", 
		"ns2_tram", 
		"ns2_refinery",
		"ns2_veil",
		"ns2_docking"
	]

urlList = [{
	'url': '/versions'
}, {
	'url': '/maps'
}, {
	'url': '/types'
}, {
	'url': '/location1'
}, {
	'url': '/location2'
}, {
	'url': '/win/pie',
	'data': {
		'version' : '*',
		'map' : '*'
	}
}, {
	'url': '/startlocationcount',
	'data': {
		'version' : '*',
		'map' : '*'
	}
}, {
	'url': '/kill/pie',
	'data': {
		'version' : '*',
		'map' : '*'
	}
}, {
	'url': '/lifetime',
	'data': {
		'version' : '*',
		'map' : '*'
	}
}]

def formatDict(dict):
	result = ""

	for k, v in dict.iteritems():
		result += k + ": " + str(v) + ", "

	return result[:-2]


class StatsComputer:

	client = Client()
	logger = logging.getLogger()

	def __init__(self):
		self.logger.setLevel(logging.INFO)
		handler = logging.StreamHandler()
		formatter = logging.Formatter("[%(asctime)s] - %(levelname)s - %(message)s")
		handler.setFormatter(formatter)

		self.logger.addHandler(handler)

	def login(self):
		self.logger.info("create temporary user")
		try:
			User.objects.get(username='casher').delete() # be sure it's removed
		except:
			pass	

		password = ''.join(random.sample(string.ascii_uppercase + string.digits,15))
		User.create_user('casher', password, 'casher@voidmail.com')
		self.client.login(username='casher', password=password)

	def logout(self):	
		self.logger.info("delete temporary user")	
		User.objects.get(username='casher').delete()


	def loadUrl(self, url, data=None):
		if data:
			return self.client.get(url, data)
		else:
			return self.client.get(url)

	def loadData(self, url):
		response = self.loadUrl(url)

		try:
			data = json.loads(response.content)
		except:
			self.logger.error("can't load " + url + " data")
			data = []

		return data


	def preprocessUrlList(self, urls):
		result = []
		versions = VERSIONS
		maps = MAPS

		for urlInfo in urls:
			url = urlInfo['url']

			if 'data' in urlInfo:
				data = urlInfo['data']

				if 'version' in data and data['version'] == '*' \
					and 'map' in data and data['map'] == '*':
					for v in versions:
						for m in maps:
							result.append({
								'url' : url,
								'data' : {
									'version': json.dumps([str(v)]),
									'map': json.dumps([str(m)])
								}
							})

					for m in maps:
						result.append({
							'url' : url,
							'data' : {
								'map': json.dumps([str(m)])
							}
						})

					for v in versions:
						result.append({
							'url' : url,
							'data' : {
								'version': json.dumps([str(v)]),
							}
						})

					result.append({
						'url' : url
					})
				else:
					result.append(urlInfo)
			else:
				result.append(urlInfo)

		self.logger.info("preprocess urls, " + str(len(result)) + " urls to cache")

		return result

	def doCache(self):
		urls = self.preprocessUrlList(urlList)
		total = len(urls)
		i = 0

		for urlInfo in urls:
			i += 1
			url = urlInfo['url']
			counter = " (" + str(i) + "/" + str(total) + ")"

			if 'data' in urlInfo:
				data = urlInfo['data']
				self.logger.info("cache " + url + " - " + formatDict(data) + counter)
				self.loadUrl(url, data)
			else:
				self.logger.info("cache " + url + counter)
				self.loadUrl(url)


	def compute(self):

		self.logger.info("clean cache")
		cache.clear()

		self.login()
		self.doCache()
		self.logout()		

if __name__ == '__main__':
	computer = StatsComputer()

	print "== START PRECOMPUTE SCRIPT =="
	computer.compute()
	print "== END PRECOMPUTE SCRIPT =="