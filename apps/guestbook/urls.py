from django.conf.urls.defaults import patterns, url
from django.conf import urls

urlpatterns = patterns('',
    url(r'^user/(?P<userid>\d*)/guestbook/$', 'apps.guestbook.views.guestbook', name='guestbook'),
    url(r'^user/(?P<userid>\d*)/guestbook/entry/(?P<id>\d*)$', 'apps.guestbook.views.guestbook', name='guestbook_entry'),
    url(r'^guestbook/conversation/(?P<sender_id>\d*)/(?P<reciver_id>\d*)/$', 'apps.guestbook.views.guestbook_conversation', name='guestbook_conversation'),
 )
