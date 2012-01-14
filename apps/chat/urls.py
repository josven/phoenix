from django.conf.urls.defaults import patterns, url
from django.conf import urls

urlpatterns = patterns('',
    url(r'^$', 'apps.chat.views.chat', name='chat'),
    
    # Return a single post
    url(r'^(?P<id>\d*)\.(?P<type>\w*)$', 'apps.chat.views.chatpost', name='chatpost'),    
    
    # Return a range posts
    url(r'^(?P<id1>\d*)-(?P<id2>\d*)\.(?P<type>\w*)$', 'apps.chat.views.chatposts', name='chatposts'),
    
    #Tinychat
     url(r'^camchat/$', 'apps.chat.views.camchat', name='camchat'),
)
