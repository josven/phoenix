# -*- coding: utf-8 -*-
import os
import datetime
from django.db import models
from django.conf import settings
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from sorl.thumbnail import ImageField
from taggit.managers import TaggableManager

GENDER_CHOICES = (
    ('O', 'Odefinerat'),
    ('M', 'Man'),
    ('K', 'Kvinna'),
    ('T', 'Transperson'),
)

class Profile(models.Model):
    """
    Profile for users.

    """
    def get_image_path(instance, filename):
        return os.path.join('avatars', str(instance.id), filename)

    user = models.OneToOneField(User)
    date_username_last_changed = models.DateTimeField(blank=True, null=True)
    name = models.CharField(max_length=150, blank=True, null=True, verbose_name="Namn")
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, verbose_name="Kön", default="O")
    birthdate = models.DateField(blank=True, null=True, verbose_name="Födelsedatum")
    description = models.TextField(blank=True, null=True, verbose_name="Beskrivning")
    location = models.CharField(max_length=50, blank=True, null=True, verbose_name="Ort")
    subscriptions = TaggableManager(verbose_name="Bevakningar")

    photo = ImageField(upload_to=get_image_path, null=True, blank=True, verbose_name="Bildfil (max 2MB)")

    @property
    def get_age(self):
        
        born = self.birthdate
        today = datetime.date.today()

        try: # raised when birth date is February 29 and the current year is not a leap year
            birthday = born.replace(year=today.year)
        except ValueError:
            birthday = born.replace(year=today.year, day=born.day-1)
        if birthday > today:
            return today.year - born.year - 1
        else:
            return today.year - born.year

    def get_absolute_url(self):
        return u'{0}'.format( reverse('read_profile', args=[self.user.id]) )

    def last_seen(self):
        return cache.get('seen_%s' % self.user.username)

    def online(self):
        if self.last_seen():
            now = datetime.datetime.now()
            if now > self.last_seen() + datetime.timedelta(seconds=settings.USER_ONLINE_TIMEOUT):
                return False
            else:
                return True
        else:
            return False

class User_Activity_log(models.Model):
    user = models.OneToOneField(User)
    last_activity_date = models.DateTimeField(auto_now_add=True)
    last_url = models.URLField()
    user_ip = models.IPAddressField()
    if_ajax = models.BooleanField()
    request_method = models.CharField(max_length=10)

    class Meta:
        verbose_name = ('User_Activity_log')
        verbose_name_plural = ('User_Activity_logs')

    

        