from django.conf.urls import url
from django.views.generic.base import RedirectView

from . import views
urlpatterns = [
    url(r'^$', RedirectView.as_view(url='latest/', permanent=False), name='index'),
    url(r'^latest/$', views.latest, name='latest'),
    url(r'^documentations/$', views.docs, name='docs'),
    url(r'^documentations/add/$', views.add, name='add'),
    url(r'^documentations/(?P<id>[0-9]+)/$', views.detail, name='detail'),
    url(r'^documentations/(?P<id>[0-9]+)/edit/$', views.edit, name='edit'),
    url(r'^documentations/(?P<id>[0-9]+)/delete/$', views.delete, name='delete'),
]
