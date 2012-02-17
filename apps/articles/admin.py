from django.contrib import admin
from models import *
import reversion

class ArticleAdmin(reversion.VersionAdmin):

    pass
    
class ArticleCommentAdmin(reversion.VersionAdmin):
    
    pass
    
admin.site.register(Article, ArticleAdmin)
admin.site.register(ArticleComment, ArticleCommentAdmin)

admin.site.register(defaultArticleCategories)
admin.site.register(ModeratorArticleCategories)