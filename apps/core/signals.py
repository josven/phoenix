# -*- coding: utf-8 -*-
from sets import Set
from django.db.models.signals import post_save
from django.dispatch import receiver

from apps.notifications.models import *

#from apps.articles.models import Article
from apps.guestbook.models import Guestbooks
from apps.forum.models import ForumComment
from apps.articles.models import ArticleComment, Article
from apps.profiles.models import Profile

from taggit.models import TaggedItem

"""

# Taggade saker
@receiver(post_save, sender=TaggedItem)
def tagged_item_reciver(sender, **kwargs):
    '''
    Denna signal skapar notifieringar när 
    saker som är taggade skapas

    Denna funkar bra
    '''

    # Tagginstansen
    instance = kwargs['instance']

    # Objektet som notifieringen handlar om, objektet som har blivit taggat
    obj = instance.content_object

    # Hämtar alla användare som har subscribat på någon av taggarna i objektet
    receivers = Profile.objects.filter(subscriptions__name__in=[instance.tag.name])

    # Skapar notifieringar för beröda användare
    for receiver in receivers:
        if receiver.user:
            notification = Notification(content_object=obj, status=0, receiver=receiver.user)
            notification.save()

# Forumkommentarer
@receiver(post_save, sender=ForumComment)
def forum_reciver(sender, **kwargs):
    
    instance = kwargs['instance']

    if instance.parent:
        # Inte en rootnod, den man svarar på är direkt parent
        receivers = [instance.parent.created_by]
    else:
        # Om detta är en root-nod så är det ett direkt svar till forumsposten
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
            if receiver:
                notification = Notification(content_object=instance, status=0, receiver=receiver)
                notification.save()

# Artikelkommentarer
@receiver(post_save, sender=ArticleComment)
def acticlecomment_reciver(sender, **kwargs):
    print "acticlecomment_reciver"
    instance = kwargs['instance']

    if instance.parent:
        # Inte en rootnod, den man svarar på är direkt parent
        receivers = [instance.parent.created_by]
    else:
        # Om detta är en root-nod så är det ett direkt svar till forumsposten
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
            if receiver:
                notification = Notification(content_object=instance, status=0, receiver=receiver)
                print "notification"
                print notification
                notification.save()

# Gästbok
@receiver(post_save, sender=Guestbooks)
def guestbook_reciver(sender, **kwargs):
    instance = kwargs['instance']

    if instance.user_id:
        notification = Notification(content_object=instance, status=0, receiver=instance.user_id)
        notification.save()
"""
