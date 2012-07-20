# -*- coding: utf-8 -*-

import datetime
from django.core.cache import cache
from django.conf import settings

from apps.profiles.models import User_Activity_log

class ActiveUserMiddleware:

    def process_request(self, request):
        current_user = request.user
        if request.user.is_authenticated():

            defaults = {
                    'last_activity_date' : datetime.datetime.now(), 
                    'last_url' : request.path_info,
                    'user_ip' : request.META.get('REMOTE_ADDR'),
                    'if_ajax' : request.is_ajax(),
                    'request_method' : request.method,
                }

            obj, created = User_Activity_log.objects.get_or_create( user=current_user, defaults = defaults )

            if obj:
                for (key, value) in defaults.items():
                    setattr(obj, key, value)
                obj.save()

            delta = datetime.timedelta(minutes=5)
            incative = datetime.datetime.now() - datetime.timedelta(minutes=5)
            request.__class__.active_users = User_Activity_log.objects.filter(last_activity_date__gt = incative, if_ajax = False)