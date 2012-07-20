# -*- coding: utf-8 -*-

from apps.core.utils import render
from apps.articles.models import Article
from django.contrib.auth.decorators import login_required
from django.contrib.contenttypes.models import ContentType
from django.views.decorators.cache import never_cache
from taggit.models import TaggedItem

@never_cache
@login_required()
def read_frontpage(request):
    
	articles = Article.active.filter(tags__name__in=["FRONTPAGE"]).select_related('created_by','created_by__profile__photo').order_by('-id')

	articles = list( articles )
	articles_ids = [article.id for article in articles]

	vars = {
		'articles' : articles,
	}

	return render(request, 'frontpage.html', vars )