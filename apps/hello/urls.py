from django.conf.urls import url, patterns
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls.static import static

from fortytwo_test_task import settings

import views

urlpatterns = [
    url(r'^$', views.user_detail, name='home'),
    url(r'^user/edit$', views.PersonEdit.as_view(), name='user_edit'),
    
    url(r'^requests$', views.request_list, name='requests'),
    url(r'^api/v1/update$', views.ajax_update, name='ajax_update'),
    url(r'^api/v1/count', views.ajax_count, name='ajax_count'),

    url(r'^accounts/login/$', 'django.contrib.auth.views.login', name='login'),
    url(r'^logout/$', 'django.contrib.auth.views.logout', name='logout'),

]
if getattr(settings, 'DEBUG'):
    urlpatterns += patterns('',) + static(settings.MEDIA_URL,
                                          document_root=settings.MEDIA_ROOT)
    urlpatterns += staticfiles_urlpatterns()
