from django.conf.urls.defaults import patterns, url
from django.conf import urls

urlpatterns = patterns('',
    url(r'^framsidan/$', 'apps.frontpage.views.read_frontpage', name='start'),
    url(r'^framsidan/$', 'apps.frontpage.views.read_frontpage', name='read_frontpage'),
 )
