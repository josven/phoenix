from django.conf.urls.defaults import patterns, url
from django.conf import urls

urlpatterns = patterns('',

    # The chat
    url(r'^$', 'apps.chat.views.chat', name='chat'),
    
    # Get chat, ajax api
    url(r'^get/$', 'apps.chat.views.get_chat', name='get_chat'),
    
    # Post chat, ajax api
    url(r'^post/$', 'apps.chat.views.post_chat', name='chat_post'),
    
    #Tinychat
     url(r'^camchat/$', 'apps.chat.views.camchat', name='camchat'),
)
