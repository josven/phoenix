from django.conf.urls.defaults import patterns, url
from django.conf import urls
from django.views.generic.simple import direct_to_template

from apps.mobile.views import ChatView
from apps.mobile.views import ChatSettingsView
from apps.mobile.views import ForumListView


urlpatterns = patterns('',
	url(r'^$', 'apps.mobile.views.start', name='mobile_root'),

    url(r'^register/$', 'apps.mobile.views.register', name='mobile_register'),
    url(r'^recover/$', 'apps.mobile.views.recover', name='mobile_recover'),
    url(r'^login/$', 'apps.mobile.views.login', name='mobile_login'),
    url(r'^about/$', 'apps.mobile.views.about', name='mobile_about'),

    url(r'^start/$', 'apps.mobile.views.start', name='mobile_start'),
    url(r'^logout/$', 'apps.mobile.views.logout', name='mobile_logout'),
    url(r'^chat/$',	ChatView.as_view(), name='mobile_chat'),
    url(r'^chat/settings/$', ChatSettingsView.as_view(), name='mobile_chat_settings'),
    url(r'^forum/$', ForumListView.as_view(), name='mobile_forum_list'),
)