from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^hello', views.hello, name='hello'),
    url(r'^new_recipe/$', views.hello),
    url(r'^login/$', views.login),
    url(r'^logout/$', views.logout),
    url(r'^register/$', views.register),
]