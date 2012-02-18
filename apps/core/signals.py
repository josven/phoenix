# -*- coding: utf-8 -*-
from sets import Set
from django.db.models.signals import post_save
from django.dispatch import receiver

from apps.notifications.models import *

#from apps.articles.models import Article
from apps.guestbook.models import Guestbooks
from apps.forum.models import ForumComment
from apps.articles.models import ArticleComment
from apps.profiles.models import Profile

from taggit.models import TaggedItem


@receiver(post_save, sender=TaggedItem)
def taggedItem_reciver(sender, **kwargs):
    instance = kwargs['instance']
    content_object = instance.content_object    
    shall_pass = ['Article']
    
    # Check if this is not a subscription tag
    if instance.content_object.__class__.__name__ in shall_pass:
        receivers = Profile.objects.filter(subscriptions__name__in=[instance.tag.name])
        for receiver in receivers:
            notification = Notification(
                type = 4, #Taggbevakning
                message = u'Tagg:"{2}" på en {0} ifrån {1}!'.format( content_object.verbose_name ,content_object.created_by.username, instance.tag.name ),
                status = 1, #NEW
                receiver = receiver.user,
                sender = content_object.created_by,
                sender_name = content_object.created_by.username,
                instance_type = content_object.__class__.__name__,
                instance_id = content_object.id,
                instance_url = content_object.get_absolute_url(),
            )

            notification.save()

@receiver(post_save, sender=Guestbooks)
def guestbook_reciver(sender, **kwargs):
    instance = kwargs['instance']

    notification = Notification(
        type = 1, #guestbook
        message = u'Gästboksinlägg ifrån {0}!'.format( instance.created_by.username ),
        status = 1, #NEW
        receiver = instance.user_id,
        sender = instance.created_by,
        sender_name = instance.created_by.username,
        instance_type = instance.__class__.__name__,
        instance_id = instance.id,
        instance_url = instance.get_absolute_url(),
        )

    notification.save()
    
@receiver(post_save, sender=ForumComment)
def forum_reciver(sender, **kwargs):
    instance = kwargs['instance']
    
    if instance.parent:
        receivers = [instance.parent.created_by]
    else:
        receivers = [instance.post.created_by]     

    # Need to notify all siblings theres a new post
    if instance.is_child_node():
        try:
            siblings = instance.get_siblings(include_self=False)
            siblings_receivers = [sibling.created_by for sibling in siblings]
            receivers += siblings_receivers
        except:
            pass
    
    # Reduce list for recivers, so no one get duplicate notifications
    receivers = sorted(set(receivers))
    
    for receiver in receivers:
        if receiver != instance.created_by:
            notification = Notification(
                type = 2, #forumcomment
                message = u'Svar i tråden "{0}"'.format( instance.post.title ),
                status = 1, #NEW
                receiver = receiver,
                sender = instance.created_by,
                sender_name = instance.created_by.username,
                instance_type = instance.__class__.__name__,
                instance_id = instance.id,
                instance_url = instance.get_absolute_url(),
                )
                
            notification.save()    


@receiver(post_save, sender=ArticleComment)
def article_reciver(sender, **kwargs):
    instance = kwargs['instance']
    
    if instance.parent:
        receivers = [instance.parent.created_by]
    else:
        receivers = [instance.post.created_by]     

    # Need to notify all siblings theres a new post
    if instance.is_child_node():
        try:
            siblings = instance.get_siblings(include_self=False)
            siblings_receivers = [sibling.created_by for sibling in siblings]
            receivers += siblings_receivers
        except:
            pass
    
    # Reduce list for recivers, so no one get duplicate notifications
    receivers = sorted(set(receivers))
    
    for receiver in receivers:
        if receiver != instance.created_by:
            notification = Notification(
                type = 3, #articleomment
                message = u'Kommentar i artiklen "{0}"'.format( instance.post.title ),
                status = 1, #NEW
                receiver = receiver,
                sender = instance.created_by,
                sender_name = instance.created_by.username,
                instance_type = instance.__class__.__name__,
                instance_id = instance.id,
                instance_url = instance.get_absolute_url(),
                )
                
            notification.save()
