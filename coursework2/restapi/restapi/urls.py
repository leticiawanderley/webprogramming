from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from film import views

urlpatterns = [
	url(r'^$', views.api_root),
    url(r'^film/$', views.FilmList.as_view(), name='film-list'),
    url(r'^film/(?P<pk>[0-9]+)/$', views.FilmDetail.as_view()),
    url(r'^film/(?P<pk>[0-9]+)/actor/$', views.ActorList.as_view()),
    url(r'^film/(?P<pk>[0-9]+)/actor/(?P<id>[0-9]+)/$', views.ActorDetail.as_view()),
    url(r'^film/(?P<pk>[0-9]+)/award/$', views.AwardList.as_view()),
    url(r'^film/(?P<pk>[0-9]+)/award/(?P<id>[0-9]+)/$', views.AwardDetail.as_view()),
    url(r'^film/(?P<pk>[0-9]+)/director/$', views.DirectorList.as_view()),
    url(r'^film/(?P<pk>[0-9]+)/director/(?P<id>[0-9]+)/$', views.DirectorDetail.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
