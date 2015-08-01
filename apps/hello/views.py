from django.shortcuts import get_object_or_404, render_to_response

from apps.hello.models import User
from fortytwo_test_task import settings


def user_detail(request):
    user = get_object_or_404(User, email=settings.ADMIN_EMAIL)
    print(user)
    return render_to_response('hello/user_detail.html', {'user': user})
