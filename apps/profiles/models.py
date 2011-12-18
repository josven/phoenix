# -*- coding: utf-8 -*-
import os
import datetime
from django.db import models
from django.contrib.auth.models import User
from sorl.thumbnail import ImageField

GENDER_CHOICES = (
    ('O', 'Obesvarat'),
    ('M', 'Kille'),
    ('T', 'Tjej'),
)

class Profile(models.Model):
    """
    Profile for users.

    """
    def get_image_path(instance, filename):
        return os.path.join('avatars', str(instance.id), filename)

    user = models.OneToOneField(User)
    name = models.CharField(max_length=150, blank=True, null=True, verbose_name="Namn")
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, verbose_name="Kön", default="O")
    birthdate = models.DateField(blank=True, null=True, verbose_name="Födelsedatum")
    description = models.TextField(blank=True, null=True, verbose_name="Beskrivning")
    location = models.CharField(max_length=50, blank=True, null=True, verbose_name="Ort")

    photo = ImageField(upload_to=get_image_path, null=True, blank=True)

    def get_absolute_url(self):
        return "/user/%s/" % self.user_id
