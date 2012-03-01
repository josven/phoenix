from django.contrib import admin
from models import *
import reversion

class ForumAdmin(reversion.VersionAdmin):

    pass
    
class ForumCommentAdmin(reversion.VersionAdmin):
    list_display = ('post', 'created_by', 'comment', 'added', 'date_last_changed',)
    list_filter = ('tags__name',)

admin.site.register(Forum, ForumAdmin)
admin.site.register(ForumComment, ForumCommentAdmin)
admin.site.register(defaultCategories)


# OLD
admin.site.register(Thread)
admin.site.register(ThreadHistory)
admin.site.register(ForumPost)
admin.site.register(ForumPostHistory)