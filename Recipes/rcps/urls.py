from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^login/$', views.login),
    url(r'^logout/$', views.logout),
    url(r'^register/$', views.register),
    url(r'^live_query_ing', views.liveIng, name='liveIng'),
    url(r'^live_query_eq', views.liveEq, name='liveEq'),
    url(r'^search', views.search, name='search'),
    url(r'^recipe/(?P<recipe_id>[0-9]+)', views.recipe, name='recipe'),
    url(r'^send_comment', views.send_comment, name='send_comment'),
    url(r'^user_page/(?P<user_id>[0-9]+)', views.user_page, name='user_page'),
    url(r'^tags', views.tags, name='tag'),
    url(r'^tag/(?P<tag_id>[0-9]+)', views.tag, name='tag'),
    url(r'^mostcommented/', views.most_commented),
    url(r'^rating', views.by_rating, name="rating"),
    url(r'^get_rating', views.get_rating, name="get_rating"),
    url(r'^add_rating', views.add_rating, name="add_rating"),
    url(r'^add_fav', views.add_favourite, name="add_fav"),
    url(r'^is_fav', views.check_favourite, name="check_fav"),
    url(r'^favourite', views.favourite, name="favourite"),
]