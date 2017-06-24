from django.conf.urls import url

from . import views
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^documentations/$', views.index, name='index'),
    url(r'^documentations/latest/$', views.latest, name='latest'),
    url(r'^documentations/add/$', views.add, name='add'),
    url(r'^documentations/(?P<id>[0-9]+)/$', views.detail, name='detail'),
    url(r'^documentations/(?P<id>[0-9]+)/edit/$', views.edit, name='edit'),
]
