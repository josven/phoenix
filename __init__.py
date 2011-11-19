from django.conf import settings
# Some extra settings

"""
   
   To enable message framework
   and enable request data in templates

"""

settings.TEMPLATE_CONTEXT_PROCESSORS += (
    'django.contrib.messages.context_processors.messages',
    'django.core.context_processors.request',
)

settings.MESSAGE_STORAGE = 'django.contrib.messages.storage.session.SessionStorage'
