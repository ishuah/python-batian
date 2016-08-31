from django.conf import settings
import requests, json, time
import threading


class Client(object):

	def __init__(self, **kwargs):
		self.APP_NAME = settings.BATIAN_APP_NAME
		self.SERVER_URL = settings.BATIAN_SERVER_URL

	def harvest(self, rawdata, category="event"):
		if category == "event":
			threading.Thread(target=self._harvest_event, args=(rawdata,)).start()	
		elif category == "exception":
			threading.Thread(target=self._harvest_exception, args=(rawdata,)).start()
			
	def _harvest_event(self, rawdata):
		"""Implemented in child classes"""
		pass

	def _harvest_exception(self, rawdata):
		"""Implemented in child classes """
		pass

	def send(self, data):
		requests.post(self.SERVER_URL, data=json.dumps(data), headers={'content-type': 'application/json'})


