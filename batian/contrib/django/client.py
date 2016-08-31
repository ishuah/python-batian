from batian.batian_api import Client
import time
from datetime import datetime


class DjangoClient(Client):

    def _harvest_event(self, rawdata):
        request, response, queries = rawdata
        if hasattr(request, "_batian_view_func"):
            view_name = self._extract_view_name(request._batian_view_func)
        else:
            view_name = None

        data = [{
                "measurement": "requests",
                "source": self.APP_NAME,
                "data": {
                    "host": request.get_host(),
                    "path": request.get_full_path(),
                    "method": request.method,
                    "view": view_name,
                    "status_code": response.status_code,
                    "response_time": time.time() - request.start_time
                },
                "timestamp": datetime.now().strftime('%Y-%m-%dT%H:%M:%SZ')
                }]

        for query in queries:
            qdata = {
                "measurement": "database_queries",
                "source": self.APP_NAME,
                "data": {
                    "host": request.get_host(),
                    "path": request.get_full_path(),
                    "sql": query['sql'].split('WHERE')[0],
                    "view": view_name,
                    "response_time": float(query['time'])
                },
                "timestamp": datetime.now().strftime('%Y-%m-%dT%H:%M:%SZ')
            }
            data.append(qdata)

        self.send(data)

    def _harvest_exception(self, rawdata):
        request, exception = rawdata

        data = [{
                "measurement": "exceptions",
                "source": self.APP_NAME,
                "data": {
                    "host": request.get_host(),
                    "path": request.get_full_path(),
                    "method": request.method,
                    "message": exception.message
                },
                "timestamp": datetime.now().strftime('%Y-%m-%dT%H:%M:%SZ')
                }]
        self.send(data)

    def _extract_view_name(self, view_func):
        module = view_func.__module__

        if hasattr(view_func, '__name__'):
            view_name = view_func.__name__
        else:
            view_name = view_func.__class__.__name__

        return '{0}.{1}'.format(module, view_name)
