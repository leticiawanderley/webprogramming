from django.conf.urls import url

from . import views

app_name = 'calculator'
urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^result/$', views.result, name='result'),
    url(r'^(?P<pk>[0-9]+)/saving/$', views.DetailView.as_view(), name='saving')
]