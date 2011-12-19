from django.conf.urls.defaults import patterns, url
from django.conf import urls

urlpatterns = patterns('',
    #All settings
    url(r'^settings$', 'apps.settings.views.read_settings', name='read_settings'),
    url(r'^(?P<appname>\w*)/settings$', 'apps.settings.views.read_settings', name='read_settings'),
)
