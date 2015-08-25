#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import logging

import time
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse_lazy, reverse
from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import get_object_or_404, render, render_to_response
from django.utils.decorators import method_decorator

from django.views.decorators.csrf import csrf_protect
from django.views.generic import UpdateView
from apps.hello.forms import UserEditForm
from apps.hello.models import Profile, RequestHistory

from django.conf import settings


logger = logging.getLogger(__name__)


def user_detail(request):
    person = get_object_or_404(Profile, email=settings.ADMIN_EMAIL)
    logger.info('Get user object')
    logger.debug(person)
    return render(request, 'hello/user_detail.html', {'person': person})


def request_list(request):
    args = ['-date']
    allowed_ordering = ['priority']
    if 'order' in request.GET and request.GET['order'] in allowed_ordering:
        args.append('-'+request.GET['order'])

    latest_requests = RequestHistory.objects\
        .exclude(path__in=[reverse('hello:ajax_update'),
                           reverse('hello:ajax_count')])\
        .order_by(*args[::-1])[:10]
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


class PersonEdit(UpdateView):
    model = Profile
    form_class = UserEditForm
    success_url = reverse_lazy('hello:user_edit')

    def get_object(self):
        object = Profile.objects.get(email=settings.ADMIN_EMAIL)
        return object

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        if getattr(settings, 'DEBUG', True) and request.POST:
            logging.info('sleep 5 sec for Ajax monitoring')
            time.sleep(5)  # delay AJAX response for s5 seconds
        return super(PersonEdit, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        if self.request.is_ajax():
            if self.request.FILES:
                self.object.photo = self.request.FILES['photo']
            self.object = form.save()
            return HttpResponse(json.dumps(self.object.as_json()),
                                content_type="application/json")
        return super(PersonEdit, self).form_valid(form)

    def form_invalid(self, form):
        if self.request.is_ajax():
            return HttpResponseBadRequest(json.dumps(form.errors),
                                          content_type="application/json")
        return super(PersonEdit, self).form_invalid(form)


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
            return HttpResponse(json.dumps({'response': False}),
                                content_type='application/json')

        if result:
            return HttpResponse(json.dumps({'response': 'OK'}),
                                content_type='application/json')
        else:
            return HttpResponse(json.dumps({'response':
                                            'Nothing to update'}),
                                content_type='application/json')
    return HttpResponse(json.dumps({'response': False}),
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
    return HttpResponse(json.dumps({'response': False}),
                        content_type='application/json')


def ajax_update_priority(request):
    if request.is_ajax() \
            and 'priority' in request.POST\
            and 'request_id' in request.POST:

            try:
                RequestHistory.objects\
                    .filter(id=request.POST['request_id'])\
                    .update(priority=request.POST['priority'])
            except Exception as e:
                print(e)
            return HttpResponse(json.dumps({'response': 'OK'}),
                                content_type='application/json')
    return HttpResponse(json.dumps({'response': False}))
        # requests = RequestHistory.objects\
        #     .filter(id__gt=request.POST['last_loaded_id'])\
        #     .filter(is_viewed=False)\
        #     .exclude(path__in=[reverse('hello:ajax_update'),
        #              reverse('hello:ajax_count')])\
        #     .all()
        #
        # last_request = RequestHistory.objects\
        #     .exclude(path__in=[reverse('hello:ajax_update'),
        #                        reverse('hello:ajax_count')])\
        #     .latest('id')
        #
        # data = {'requests': [ob.as_json() for ob in requests],
        #         'count': requests.count(),
        #         'last_request': last_request.id}

        # return HttpResponse(json.dumps(data), content_type='application/json')
    # return HttpResponse(json.dumps({'response': 'False'}),
    #                     content_type='application/json')