from client import DjangoClient
from django.db import connection
import time


class BatianAPMMiddleware(object):

    def __init__(self, **kwargs):
        self.client = DjangoClient()

    def process_request(self, request):
        request.start_time = time.time()

    def process_view(self, request, view_func, view_args, view_kwargs):
        request._batian_view_func = view_func

    def process_response(self, request, response):
        self.client.harvest((request, response, connection.queries))
        return response

    def process_exception(self, request, exception):
        self.client.harvest((request, exception), category="exception")
