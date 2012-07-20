from django.conf.urls.defaults import patterns, url
from django.conf import urls

urlpatterns = patterns('',
    url(r'^user/(?P<userid>\d*)/guestbook/$', 'apps.guestbook.views.guestbook', name='guestbook'),
    url(r'^user/(?P<userid>\d*)/guestbook/entry/(?P<id>\d*)/$', 'apps.guestbook.views.guestbook_entry', name='guestbook_entry'),
    url(r'^user/(?P<userid>\d*)/guestbook/entry/(?P<id>\d*)/delete/$', 'apps.guestbook.views.guestbook_entry_delete', name='guestbook_entry_delete'),
    url(r'^guestbook/conversation/(?P<sender_id>\d*)/(?P<reciver_id>\d*)/$', 'apps.guestbook.views.guestbook_conversation', name='guestbook_conversation'),
    url(r'^guestbook/conversation/(?P<sender_id>\d*)/(?P<reciver_id>\d*)/entry/(?P<id>\d*)/$', 'apps.guestbook.views.guestbook_conversation', name='guestbook_conversation_entry'),
 )
