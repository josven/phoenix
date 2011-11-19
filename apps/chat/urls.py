from django.conf.urls.defaults import patterns, url
from django.conf import urls

urlpatterns = patterns('',
    url(r'^$', 'apps.chat.views.chat', name='chat'),
)
