from django.conf.urls import url
from django.views.generic.base import RedirectView

from . import views
urlpatterns = [
    url(r'^$', RedirectView.as_view(url='latest/', permanent=False), name='index'),
    url(r'^latest/$', views.latest, name='latest'),
    url(r'^documentations/$', views.docs, name='docs'),
    url(r'^documentations/add/$', views.doc_add, name='doc_add'),
    url(r'^documentations/(?P<id>[0-9]+)/$', views.doc_detail, name='doc_detail'),
    url(r'^documentations/(?P<id>[0-9]+)/edit/$', views.doc_edit, name='doc_edit'),
    url(r'^documentations/(?P<id>[0-9]+)/delete/$', views.doc_delete, name='doc_delete'),
    url(r'^keywords/$', views.words, name='words'),
    url(r'^keywords/(?P<id>[0-9]+)/$', views.word_detail, name='word_detail'),
    url(r'^keywords/(?P<id>[0-9]+)/edit/$', views.word_edit, name='word_edit'),
    url(r'^keywords/(?P<id>[0-9]+)/delete/$', views.word_delete, name='word_delete'),
]
