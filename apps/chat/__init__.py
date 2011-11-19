import os
from django.conf import settings
settings.TEMPLATE_DIRS += (os.path.dirname(__file__)+'/templates/',)
settings.STATICFILES_DIRS += (os.path.dirname(__file__)+'/static/',)