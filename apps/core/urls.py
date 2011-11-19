from django.conf.urls.defaults import patterns, url
from django.conf import urls

urlpatterns = patterns('',
    url(r'^setbase/(?P<base>\w*)/$', 'apps.core.utils.set_base_template', name='set_base_template'),
)
