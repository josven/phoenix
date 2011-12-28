from django.contrib import admin
from models import *

admin.site.register(Article)
admin.site.register(defaultArticleCategories)
admin.site.register(ModeratorArticleCategories)