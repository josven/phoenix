# -*- coding: utf-8 -*-

import copy

from django import template

from apps.notifications import models

register = template.Library()

@register.assignment_tag(takes_context=True)
def get_notes_for_annoncements(context, user):
    print "get_notes_for_annoncements"

    notifications = user.receiver_entries.filter(status = 0)
    notifications.update( status = 1 )
    print "notifications"
    print notifications

    return notifications


# I aktivitetsfönsteret så sätter vi nya notificationer som olästa
@register.assignment_tag()
def set_notifications_to_unread( notifications ):

    notes = list( notifications )
    old_notifications = copy.deepcopy( notes )
    new_notifications = _set_min_status_on_qs( notes )

    return old_notifications

# När man öppnar framsidan så lägger man på alla notes till artiklarna
# Samt sparar tar bort dem, efersom de är nu läsra
@register.assignment_tag(takes_context=True)
def get_notes_for_articlelist(context, queryset, user):
    
    notifications = _get_notifications_for_qs(queryset, user)
    queryset = _assign_notifications_on_qs(queryset, notifications)
    new_notifications = _delete_notifications(notifications)

    return queryset

# När man öppnar gäsrboken så lägger man på alla notes till gärstboksinläggen
# Samt sparar alla notes som obesvarade
@register.assignment_tag(takes_context=True)
def get_notes_for_guestbook(context, queryset, user):
    
    notifications = _get_notifications_for_qs(queryset, user)
    queryset = _assign_notifications_on_qs(queryset, notifications)
    new_notifications = _set_status_on_qs(notifications, 3)

    return queryset

# När man öppnar en artikel så lägger man på alla notes till arikelkommentarerna
# Samt sparar alla notes som obesvarade
@register.assignment_tag(takes_context=True)
def get_notes_for_article_comments(context, queryset, user):
    
    notifications = _get_notifications_for_qs(queryset, user)
    queryset = _assign_notifications_on_qs(queryset, notifications)
    new_notifications = _set_status_on_qs(notifications, 3)

    return queryset


@register.assignment_tag(takes_context=True)
def get_notes_for_item(context, item, user):
    
    note = _get_notification_for_item(item, user)
    item = _assign_notifications_on_item(item, note)
    new_note = _set_status_on_qs(note, 3)

    return item


# -------------------------------------------------------------------------------------------------------------


def _get_notification_for_item(item, user):
    return user.receiver_entries.filter(content_type__model = item.__class__.__name__.lower(), object_id = item.id)

def _get_notifications_for_qs(itemlist, user):
    ids = [item.id for item in itemlist]
    return user.receiver_entries.filter(content_type__model = itemlist[0].__class__.__name__.lower(), object_id__in = ids)



def _assign_notifications_on_item(item, notification):
    if notification:
        item.notification = copy.copy(notification[0])
        print item.notification
    return item

def _assign_notifications_on_qs(itemlist, notifications):
    for notification in notifications:
        for item in itemlist:
            if item.id == notification.object_id:
                item.notification = copy.copy(notification)
                print item.notification
    return itemlist



def _set_status_on_item(item, status):
    item.status = int( float ( status ) )
    item.save()
    return item

def _set_status_on_qs(itemlist, status):
    for item in itemlist:
        item.status = int( float ( status ) )
        item.save()
    return itemlist

def _set_min_status_on_qs(itemlist):
    for item in itemlist:
        if item.status == 1:
            item.status = 2
        item.save()
    return itemlist

def _delete_notifications(itemlist):
    for item in itemlist:
        item.delete()
    return None
