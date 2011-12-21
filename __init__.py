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

settings.TEMPLATE_LOADERS += (
    'django.template.loaders.app_directories.load_template_source',
)

# clear cache, this if testing, not to use in production
from django.core.cache import cache
cache.clear()