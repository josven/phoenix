from django.conf.urls.defaults import patterns, url
from django.conf import urls

urlpatterns = patterns('',
    url(r'^$', 'apps.forum.views.read_forum', name='read_forum'),
    url(r'^thread/create/$', 'apps.forum.views.create_thread', name='create_thread'),
)
