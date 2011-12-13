from django.contrib import admin
from models import Thread, ThreadHistory, ForumPost, ForumPostHistory

admin.site.register(Thread)
admin.site.register(ThreadHistory)
admin.site.register(ForumPost)
admin.site.register(ForumPostHistory)
