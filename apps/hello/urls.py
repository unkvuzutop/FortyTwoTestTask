from django.conf.urls import url

import views

urlpatterns = [
    url(r'^$', views.user_detail, name='home'),
    # url(r'^products/$', views.products, name='products'),
    # url(r'^products/(?P<slug>[\w-]+)/$', views.product_detail,
    #     name='product_detail'),
    # url(r'^signup/$', views.sign_up, name='sign_up'),
    # url(r'^signin/$', views.sign_in, name='sign_in'),
    # url(r'^signout/$', views.sign_out, name='sign_out'),
    # url(r'^like/(?P<product_id>[0-9]+)$', views.like_product, name='like')
]