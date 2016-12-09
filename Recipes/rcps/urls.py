from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^new_recipe/$', views.hello),
    url(r'^login/$', views.login),
    url(r'^logout/$', views.logout),
    url(r'^register/$', views.register),
    url(r'^live_query_ing', views.liveIng, name='liveIng'),
    url(r'^live_query_eq', views.liveEq, name='liveEq'),
    url(r'^search', views.search, name='search')
]