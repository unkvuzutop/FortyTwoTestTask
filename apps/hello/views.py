from django.shortcuts import render, get_object_or_404, render_to_response

# Create your views here.
from django.template import RequestContext
from django.views.generic.detail import DetailView
from apps.hello.models import User
from fortytwo_test_task import settings


def user_detail(request):
    user = get_object_or_404(User, email=settings.ADMIN_EMAIL)
    print(user)
    return render_to_response('hello/user_detail.html', {'user':user})