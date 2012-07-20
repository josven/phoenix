# -*- coding: utf-8 -*-

from django.conf.urls.defaults import patterns, url
from django.conf import urls

urlpatterns = patterns('',    

     url(r'^$', 'apps.notifications.views.notifications', name='read_notifications'),
     url(r'^delete/$', 'apps.notifications.views.delete_notification', name='delete_notification'),
     url(r'^delete/$', 'apps.notifications.views.delete_notification', name='delete_notifications'),
     url(r'^updates.(?P<format>\w*)$', 'apps.notifications.views.updates', name='read_updates'),

)
