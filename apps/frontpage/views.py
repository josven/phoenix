from apps.core.utils import render
from apps.articles.models import Article
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache

@never_cache
@login_required(login_url='/auth/login/')
def read_frontpage(request):
    
    vars = {
        'articles' : Article.active.filter(tags__name__in=["FRONTPAGE"]).order_by('-id'),
        }

    return render(request, 'frontpage.html', vars )