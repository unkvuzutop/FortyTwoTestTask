import logging
from apps.hello.models import RequestHistory

logger = logging.getLogger(__name__)


def exclude_request_tracing(f):
    def _exclude_request_tracing(*args, **kwargs):
        return f(*args, **kwargs)
    return _exclude_request_tracing


class CatchRequest(object):
    @staticmethod
    def save_request(request):
        data = {'path': request.path,
                'host': request.get_host(),
                'ip': request.META['REMOTE_ADDR'],
                'method': request.method}

        request_row = RequestHistory(**data)

        try:
            request_row.save()
        except Exception as e:
            logger.info('Error while saving the request to the server')
            logger.error(e)
        else:
            logger.info('Request saved seccessfuly')
            logger.debug(getattr(request_row, 'path'))

    def process_view(self, request, view_func, view_args, view_kwargs):
        if view_func.func_name != "_exclude_request_tracing":
            self.save_request(request)
        return view_func(request, *view_args, **view_kwargs)
