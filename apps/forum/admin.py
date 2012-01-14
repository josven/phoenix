from django.contrib import admin
from models import *

admin.site.register(Forum)
admin.site.register(ForumComment)

admin.site.register(Thread)
admin.site.register(ThreadHistory)
admin.site.register(ForumPost)
admin.site.register(ForumPostHistory)
admin.site.register(defaultCategories)
