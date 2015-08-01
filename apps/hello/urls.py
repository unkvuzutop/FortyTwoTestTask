from django.conf.urls import url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

import views

urlpatterns = [
    url(r'^$', views.user_detail, name='home'),
]

urlpatterns += staticfiles_urlpatterns()
