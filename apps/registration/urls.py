from django.conf.urls.defaults import patterns, url
from django.conf import urls

urlpatterns = patterns('',
    url(r'^login/$', 'apps.registration.views.auth_login', name='login'),
    url(r'^logout/$', 'apps.registration.views.auth_logout', name='logout'),
)
