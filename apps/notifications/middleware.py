# -*- coding: utf-8 -*-

from django.contrib import messages
from django.core.urlresolvers import reverse
from django.utils.encoding import force_unicode

from apps.notifications.models import *


class AnnonuceNotifications(object):
    def process_view(self, request, view_func, view_args, view_kwargs):
        if not request.is_ajax():
            if request.user.is_authenticated():

                notifications = request.user.receiver_entries.filter(status__in=[0, 1])
                notification_count = len(notifications)

                announced_notifications = [note for note in notifications if note.status in [0]]
                announced_notifications_length = len(announced_notifications)

                #new_notifications = [note for note in notifications if note.status in [1]]
                #new_notifications_length = len(new_notifications)

                if announced_notifications_length == 1:
                    if note.content_object:
                        note = announced_notifications[0]
                        name = force_unicode(getattr(note.content_object, 'get_verbose_name', None))
                        url = force_unicode(note.content_object.get_absolute_url())
                        message = u'Ny aktivitet!<br/> {0} </br> <a href="{1}">Gå dit</a>'.format(name, url)

                if announced_notifications_length > 1:
                    message = u'{0} nya aktiviteter!<br/> <a href="{1}">Gå dit</a>'.format(announced_notifications_length, reverse('read_notifications'))

                if announced_notifications_length != 0:
                    messages.add_message(request, messages.INFO, message)

                for a_note in announced_notifications:
                    a_note.status = 1
                    a_note.save()

                request.__class__.notification_count = notification_count

        return None
