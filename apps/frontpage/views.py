from apps.core.utils import render
from apps.articles.models import Article
from django.contrib.auth.decorators import login_required

@login_required(login_url='/auth/login/')
def read_frontpage(request):
    
    vars = {
        'articles' : Article.objects.filter(tags__name__in=["FRONTPAGE"])
        }
    test = articles = Article.active.filter(tags__name__in=["FRONTPAGE"])
    print test
    return render(request, 'frontpage.html', vars )