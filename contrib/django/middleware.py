import requests, json, time, re
from django.conf import settings
from django.db import connection
from tomorrow import threads

class CatchMiddleware(object):
	SERVER_URL = 'http://localhost:5000/write_data/'
	
	def process_request(self, request):
		request.start_time = time.time()

	def process_response(self, request, response):
		self.log_event(request, response, connection.queries)
		return response

	def process_exception(request, exception):
		self.log_exception(request, exception)

	@threads(3)
	def log_event(self, request, response, queries):
		
		data = [{
				"measurement": "requests",
				"tags": {
					"app": settings.BATIAN_APP_NAME,
					"host": request.get_host(),
					"path": request.get_full_path(),
					"method": request.method
				},
				"fields": {
					"status_code": response.status_code,
					"response_time": time.time() - request.start_time
				}
			}]
		for query in queries:
			extract = re.findall('"([^"]*)"', query['sql'])
			table = extract[0] + "." + extract[1]
			qdata = {
				"measurement": "database_queries",
				"tags": {
					"app": settings.BATIAN_APP_NAME,
					"host": request.get_host(),
					"path": request.get_full_path(),
					"table": table
				},
				"fields": {
					"response_time": float(query['time'])
				}
			}

			data.append(qdata)
		requests.post(SERVER_URL, data=json.dumps(data), headers={'content-type': 'application/json'})


	@threads(5)
	def log_exception(self, request, exception):
		data = [{
				"measurement": "exceptions",
				"tags": {
					"app": settings.BATIAN_APP_NAME,
					"host": request.get_host(),
					"path": request.get_full_path(),
					"method": request.method,
					"message": exception.message
				},
				"fields": {
					"fatal": 1
				}
			}]
		requests.post(SERVER_URL, data=json.dumps(data), headers={'content-type': 'application/json'})