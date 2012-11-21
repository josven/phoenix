# -*- coding: utf-8 -*-

from django.db import models

from django.contrib.auth.models import User

class mobile_settings(models.Model):
	user = models.OneToOneField(User, related_name="mobile_user_settings")
	chat_textile = models.BooleanField( verbose_name = "Visa Textile formatering" )
	chat_oembed = models.BooleanField( verbose_name = "Visa inbäddat innehåll" )
	chat_urlize = models.BooleanField( verbose_name = "Visa klickbara länkar" )

