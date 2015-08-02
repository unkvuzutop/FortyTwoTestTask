from django.conf.urls import url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

import views

urlpatterns = [
    url(r'^$', views.user_detail, name='home'),
    url(r'^requests$', views.request_list, name='requests'),
    url(r'^api/v1/update$', views.ajax_update, name='ajax_update'),
    url(r'^api/v1/count', views.ajax_count, name='ajax_count')
]

urlpatterns += staticfiles_urlpatterns()
