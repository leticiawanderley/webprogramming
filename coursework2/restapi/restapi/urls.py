from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from film import views

urlpatterns = [
	url(r'^$', views.api_root),
    url(r'^film/$', views.FilmList.as_view(), name='film-list'),
    url(r'^film/(?P<pk>[0-9]+)/$', views.FilmDetail.as_view(), name='film-detail'),
    url(r'^film/(?P<pk>[0-9]+)/actor/$', views.ActorList.as_view(), name='actor-list'),
    url(r'^film/(?P<pk>[0-9]+)/award/$', views.AwardList.as_view(), name='award-list'), 
    url(r'^film/(?P<pk>[0-9]+)/director/$', views.DirectorList.as_view(), name='director-list'),
    url(r'^actor/$', views.ActorList.as_view(), name='actor-list'),
    url(r'^actor/(?P<pk>[0-9]+)/$', views.ActorDetail.as_view(), name='actor-detail'),
    url(r'^award/$', views.AwardList.as_view(), name='award-list'),
    url(r'^award/(?P<pk>[0-9]+)/$', views.AwardDetail.as_view(), name='award-detail'),
    url(r'^director/$', views.DirectorList.as_view(), name='director-list'),
    url(r'^director/(?P<pk>[0-9]+)/$', views.DirectorDetail.as_view(), name='director-detail'),
]

urlpatterns = format_suffix_patterns(urlpatterns)
