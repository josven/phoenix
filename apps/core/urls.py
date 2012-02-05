from django.conf.urls.defaults import patterns, url
from django.conf import urls

urlpatterns = patterns('',
    url(r'^utils/preview/$', 'apps.core.views.preview', name='preview'),
)
