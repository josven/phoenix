from django.conf.urls.defaults import patterns, url
from django.conf import urls

urlpatterns = patterns('',
    url(r'^$', 'apps.forum.views.list_forum', name='list_forum'),
)
