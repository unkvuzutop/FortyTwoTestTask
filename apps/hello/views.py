#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import logging
import time
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse_lazy
from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import get_object_or_404, render
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect
from django.views.generic import UpdateView
from apps.hello.forms import UserEditForm
from apps.hello.models import Profile, RequestHistory

from fortytwo_test_task import settings

logger = logging.getLogger(__name__)


def user_detail(request):
    person = get_object_or_404(Profile, email=settings.ADMIN_EMAIL)
    logger.info('Get user object')
    logger.debug(person)
    return render(request, 'hello/user_detail.html', {'person': person})


def request_list(request):
    latest_requests = RequestHistory.objects\
        .order_by('-date')[:10]
    last_request = RequestHistory.objects.latest('id')

    return render(request, 'hello/requests.html',
                  {'latest_requests': latest_requests,
                   'last_request': last_request})


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
                .update(is_viewed=True)
            if not result:
                    return HttpResponse('{"response": "Nothing to update"}',
                                        content_type='application/json')
        except Exception as e:
            logging.info('can\'t update object')
            logging.error(e)
            return HttpResponse('{"response": "False"}',
                                content_type='application/json')

        return HttpResponse('{"response": "OK"}',
                            content_type='application/json')
    return HttpResponse('{"response": "False"}',
                        content_type='application/json')


@csrf_protect
def ajax_count(request):
    if request.is_ajax() and 'last_loaded_id' in request.POST:
        requests = RequestHistory.objects\
            .filter(id__gt=request.POST['last_loaded_id'])\
            .filter(is_viewed=False)\
            .all()

        last_request = RequestHistory.objects.latest('id')
        data = {'requests': [ob.as_json() for ob in requests],
                'count': requests.count(),
                'last_request': last_request.id}

        return HttpResponse(json.dumps(data), content_type="application/json")
    return HttpResponse('{"response": "False"}',
                        content_type='application/json')
