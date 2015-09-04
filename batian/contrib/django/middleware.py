import requests, json, time, re
from django.conf import settings
from django.db import connection
from tomorrow import threads

class CatchMiddleware(object):

	def __init__(self, **kwargs):
		self.SERVER_URL = 'http://localhost:3000/log/'
	
	def process_request(self, request):
		request.start_time = time.time()

	def process_view(self, request, view_func, view_args, view_kwargs):
		request._batian_view_func = view_func

	def process_response(self, request, response):
		self._log_event(request, response, connection.queries)
		return response

	def process_exception(self, request, exception):
		self._log_exception(request, exception)

	@threads(3)
	def _log_event(self, request, response, queries):
		view_name = self._extract_view_name(request._batian_view_func)
		data = [{
				"measurement": "requests",
				"data": {
					"app": settings.BATIAN_APP_NAME,
					"host": request.get_host(),
					"path": request.get_full_path(),
					"method": request.method,
					"view": view_name,
					"status_code": response.status_code,
					"response_time": time.time() - request.start_time
				},
				"timestamp": int(round(time.time()*1000))
			}]
		for query in queries:
			qdata = {
				"measurement": "database_queries",
				"data": {
					"app": settings.BATIAN_APP_NAME,
					"host": request.get_host(),
					"path": request.get_full_path(),
					"sql": query['sql'].split('WHERE')[0],
					"view": view_name,
					"response_time": float(query['time'])
				},
				"timestamp": int(round(time.time()*1000))
			}

			data.append(qdata)
		
		requests.post(self.SERVER_URL, data=json.dumps(data), headers={'content-type': 'application/json'})


	@threads(3)
	def _log_exception(self, request, exception):
		data = [{
				"measurement": "exceptions",
				"data": {
					"app": settings.BATIAN_APP_NAME,
					"host": request.get_host(),
					"path": request.get_full_path(),
					"method": request.method,
					"message": exception.message
				},
				"timestamp": int(round(time.time()*1000))
			}]
		requests.post(self.SERVER_URL, data=json.dumps(data), headers={'content-type': 'application/json'})

	def _extract_view_name(self, view_func):
		module = view_func.__module__

		if hasattr(view_func, '__name__'):
			view_name = view_func.__name__
		else:  
			view_name = view_func.__class__.__name__

		return '{0}.{1}'.format(module, view_name)