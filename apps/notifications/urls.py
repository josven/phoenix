# -*- coding: utf-8 -*-

from django.conf.urls.defaults import patterns, url
from django.conf import urls

urlpatterns = patterns('',    

     url(r'^updates.(?P<format>\w*)', 'apps.notifications.views.updates', name='read_updates'),
)
