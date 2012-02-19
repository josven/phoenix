from django.conf.urls.defaults import patterns, url
from django.conf import urls

urlpatterns = patterns('',
    url(r'^old$', 'apps.forum.views.read_old_forum', name='read_forum'),
    
    url(r'^thread/create/$', 'apps.forum.views.create_thread', name='create_thread'),
    url(r'^thread/create/(?P<tags>(.+)(,\s*.+)*)/', 'apps.forum.views.create_thread', name='create_thread_by_tags'),

    url(r'^thread/read/(?P<id>\d*)/$', 'apps.forum.views.read_thread', name='read_thread'),
    
    url(r'^tags/(?P<tags>(.+)(,\s*.+)*)/$', 'apps.forum.views.get_threads_by_tags', name='get_threads_by_tags'),


    url(r'^forumpost/create/$', 'apps.forum.views.create_forumpost', name='create_forumpost'),
    
    url(r'^forumpost/reply/$', 'apps.forum.views.create_forumpost', name='reply_on_forumpost'),
    url(r'^forumthread/reply/$', 'apps.forum.views.create_forumpost', name='reply_on_thread'),
    
    
    #json for datatables
    url(r'^list/json/$', 'apps.forum.views.list_forum_json', name='list_forum_json'),
    url(r'^tag/(?P<tags>(.+)(,\s*.+)*)/json/$', 'apps.forum.views.list_forum_json', name='list_forum_json'),    
    
    
    
    url(r'^list/$', 'apps.forum.views.list_forum', name='list_forum'),
    url(r'^tag/(?P<tags>(.+)(,\s*.+)*)/$', 'apps.forum.views.list_forum', name='list_forum'),
    
    url(r'^read/(?P<id>\d*)/$', 'apps.forum.views.read_forum', name='read_forum'),
    
    url(r'^create/(?P<tags>(.+)(,\s*.+)*)/$', 'apps.forum.views.create_forum', name='create_forum'),
    url(r'^create/$', 'apps.forum.views.create_forum', name='create_forum'),
    
        
    url(r'^read/(?P<forum_id>\d*)/comment/$', 'apps.forum.views.comment_forum', name='comment_forum'),


    
)
