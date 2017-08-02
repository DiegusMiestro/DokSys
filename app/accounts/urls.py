from django.conf.urls import url

from . import views
urlpatterns = [
    url(r'^login/$', views.login, name='login'),
    url(r'^logout/$', views.logout, name='logout'),
    url(r'^users/$', views.users, name='users'),
    url(r'^users/(?P<id>[0-9]+)/$', views.detail, name='detail'),
    url(r'^users/add/$', views.add, name='add'),
    url(r'^users/(?P<id>[0-9]+)/edit/$', views.edit, name='edit'),
    url(r'^users/(?P<id>[0-9]+)/active/$', views.active, name='active'),
    url(r'^users/(?P<id>[0-9]+)/desactive/$', views.desactive, name='desactive'),
    url(r'^profile/$', views.profile, name='profile'),
    url(r'^profile/edit/$', views.profile_edit, name='profile_edit'),
]
