import logging
from apps.hello.models import RequestHistory


class CatchRequest(object):
    @staticmethod
    def save_request(request):
        request_row = RequestHistory(
            path=request.path,
            host=request.get_host(),
            ip=request.META['REMOTE_ADDR'],
            method=request.method)
        try:
            request_row.save()
        except:
            logging.error('Error while saving the request to the server')

    def process_request(self, request):
        self.save_request(request)
