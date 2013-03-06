# -*- coding: utf-8 -*-
from django.db.models.signals import post_save
from django.dispatch import receiver

from apps.notifications.models import *
from django.contrib.auth.models import User
#from apps.articles.models import Article
from apps.guestbook.models import Guestbooks
from apps.forum.models import ForumComment
from apps.articles.models import ArticleComment, Article
from apps.profiles.models import Profile

from taggit.models import TaggedItem

# Taggade saker
@receiver(post_save, sender=TaggedItem)
def tagged_item_reciver(sender, **kwargs):
    '''
    Denna signal skapar notifieringar när 
    saker som är taggade skapas

    Denna funkar bra
    '''
    print "TAGG"

    # Tagginstansen
    instance = kwargs['instance']

    # Objektet som notifieringen handlar om, objektet som har blivit taggat
    obj = instance.content_object

    # Inga profile objects
    if not obj.__class__.__name__ == "Profile":

        # Användaren som har skapat objektet
        created_by = obj.created_by

        # Hämtar alla användarprofiler som har subscribat på någon av taggarna i objektet
        receivers_profiles = Profile.objects.select_related('user__receiver_entries','user__id','user','subscriptions__name').filter(subscriptions__name__in=[instance.tag.name])

        # Exluderar den som skapade objektet
        receivers_profiles = receivers_profiles.exclude(user__id = created_by.id)

        # Skapar notifieringar för beröda användare
        for receiver in receivers_profiles:
            if receiver.user:

                # Hämtar gamla notifikationerna för användaren
                ctype_model = obj.__class__.__name__.lower()
                if not receiver.user.receiver_entries.filter(content_type__model = ctype_model, object_id = obj.id):
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
