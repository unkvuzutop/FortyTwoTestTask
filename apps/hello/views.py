import json
import logging
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render_to_response
from django.views.decorators.csrf import csrf_protect
from apps.hello.models import Profile, RequestHistory
from apps.hello.middleware import exclude_request_tracing
from apps.hello.utils import get_unreaded_requests_count

from django.conf import settings

logger = logging.getLogger(__name__)


def user_detail(request):
    user = get_object_or_404(Profile, email=settings.ADMIN_EMAIL)
    logger.info('Get user object')
    logger.debug(user)
    return render_to_response('hello/user_detail.html', {'user': user})


def request_list(request):
    latest_requests = RequestHistory.objects\
        .order_by('-date')[:10]

    latest_requests_count = get_unreaded_requests_count(latest_requests)

    return render_to_response('hello/requests.html',
                              {'latest_requests': latest_requests,
                               'latest_requests_count': latest_requests_count})


@csrf_protect
@exclude_request_tracing
def ajax_update(request):
    if request.is_ajax() and request.method == 'POST':
        viewed_request_id = request.POST['viewed']
        try:
            result = RequestHistory.objects\
                .filter(id__in=viewed_request_id.split(','))\
                .update(is_viewed=True)
        except Exception as e:
            logging.info('can\'t update object')
            logging.error(e)
            return HttpResponse(json.dumps({'response': 'False'}),
                                content_type='application/json')

        if result:
            return HttpResponse(json.dumps({'response': 'OK'}),
                                content_type='application/json')
        else:
            return HttpResponse(json.dumps({'response':
                                            'Nothing to update'}),
                                content_type='application/json')
    return HttpResponse(json.dumps({'response': 'False'}),
                        content_type='application/json')


@csrf_protect
@exclude_request_tracing
def ajax_count(request):
    if request.is_ajax():
        requests = RequestHistory.objects\
            .order_by('-date')[:10]

        last_request = RequestHistory.objects.latest('id')

        data = {'requests': [ob.as_json() for ob in requests],
                'count': get_unreaded_requests_count(requests)}
        return HttpResponse(json.dumps(data), content_type='application/json')
    return HttpResponse(json.dumps({'response': 'False'}),
                        content_type='application/json')
