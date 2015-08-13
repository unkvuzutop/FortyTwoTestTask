import json
import logging
from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render_to_response
from django.views.decorators.csrf import csrf_protect
from apps.hello.models import Profile, RequestHistory

from django.conf import settings


logger = logging.getLogger(__name__)


def user_detail(request):
    user = get_object_or_404(Profile, email=settings.ADMIN_EMAIL)
    logger.info('Get user object')
    logger.debug(user)
    return render_to_response('hello/user_detail.html', {'user': user})


def request_list(request):
    latest_requests = RequestHistory.objects\
        .exclude(path__in=[reverse('hello:ajax_update'),
                           reverse('hello:ajax_count')])\
        .order_by('-date')[:10]
    last_request = RequestHistory.objects\
        .exclude(path__in=[reverse('hello:ajax_update'),
                           reverse('hello:ajax_count')])\
        .latest('id')

    latest_requests_count = 0
    for request in latest_requests:
        if not request.is_viewed:
            latest_requests_count += 1

    return render_to_response('hello/requests.html',
                              {'latest_requests': latest_requests,
                               'last_request': last_request,
                               'latest_requests_count': latest_requests_count})


@csrf_protect
def ajax_update(request):
    if request.is_ajax() and request.method == 'POST':
        viewed_request_id = request.POST['viewed']
        try:
            result = RequestHistory.objects\
                .filter(id__in=viewed_request_id.split(','))\
                .exclude(path__in=[reverse('hello:ajax_update'),
                         reverse('hello:ajax_count')])\
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
def ajax_count(request):
    if request.is_ajax() and 'last_loaded_id' in request.POST:
        requests = RequestHistory.objects\
            .filter(id__gt=request.POST['last_loaded_id'])\
            .filter(is_viewed=False)\
            .exclude(path__in=[reverse('hello:ajax_update'),
                     reverse('hello:ajax_count')])\
            .all()

        last_request = RequestHistory.objects\
            .exclude(path__in=[reverse('hello:ajax_update'),
                               reverse('hello:ajax_count')])\
            .latest('id')

        data = {'requests': [ob.as_json() for ob in requests],
                'count': requests.count(),
                'last_request': last_request.id}

        return HttpResponse(json.dumps(data), content_type='application/json')
    return HttpResponse(json.dumps({'response': 'False'}),
                        content_type='application/json')
