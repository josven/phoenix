# -*- coding: utf-8 -*-
from models import *
from forms import *
from django.contrib import messages
from django.contrib.auth.models import User, Group
from django.contrib.auth.decorators import login_required, permission_required
from django.views.decorators.cache import never_cache
from django.http import Http404, HttpResponseRedirect
from apps.core.utils import render
from django.core.urlresolvers import reverse

"""
Articles

"""

@never_cache
@login_required(login_url='/auth/login/')
def create_article(request):
    """
    Create article
    
    """
    form = ArticleForm()
    
    vars = {
        'form':form,
        'categories':defaultArticleCategories.objects.all(),
        'moderator_categories': ModeratorArticleCategories.objects.all(),
        }
    
    if request.method == 'POST':
        form = ArticleForm(request.POST)
        vars['form'] = form
        
        if form.is_valid():
            
            post_values = request.POST.copy()
            tags = ""

            for tag in post_values['tags'].split():
                
                is_upper = tag.isupper()
                is_staff = request.user.is_staff
                
                if is_upper and is_staff:
                    tags += " " + tag.upper()
                else:
                    tags += " " + tag.lower()

            post_values['tags'] = tags.strip()
            form = ArticleForm(post_values)         
            link = form.save()

            return HttpResponseRedirect(reverse('read_article', args=[link.id]))
            
    return render(request,'create_article.html', vars)

@never_cache
@login_required(login_url='/auth/login/')
def update_article(request,id):
    """
    Update article
    
    """
    vars = {}
    
    return render(request,'article.html', vars)
    
@never_cache
@login_required(login_url='/auth/login/')
def read_article(request,id=None):
    """
    Read article
    
    """
    vars = {
        'categories': defaultArticleCategories.objects.all(),
        }
    
    if id==None:
        """
        return all articles
        """
        vars['articles'] = Article.objects.all()
        
        return render(request,'articles.html', vars)
    
    vars['article'] = Article.objects.get(id=id)
    
    return render(request,'article.html', vars)

@never_cache
@login_required(login_url='/auth/login/')
def delete_article(request,id):
    """
    Delete article
    
    """
    vars = {}
    
    return render(request,'article.html', vars)
    

@never_cache
@login_required(login_url='/auth/login/')
def search_article(request, tags=None, user_id=None):
    """
    Search articles by tags
    
    Lower cap all tags, to its not 
    possible to get INTERNAL TAGS in
    the serach results
    """

    categories = defaultArticleCategories.objects.all()

    tags = [x.lower() for x in tags.split(",")]
    
    if user_id and tags:
        articles = Article.active.filter(tags__name__in=tags, created_by__id = user_id)
    
    if tags and not user_id:
        articles = Article.active.filter(tags__name__in=tags)
    else:
        Article.active.all()
        
    if len( articles ) < 1:
        messages.add_message(request, messages.INFO, 'Hittade inga artiklar =(')

    return render(request, 'articles.html', {"articles": articles,"categories":categories})
    
    
    
    

@never_cache    
@login_required(login_url='/auth/login/')
def ajax_article_body_form(request,id=None):
    user = request.user
    article = Article.objects.get(id=id)
    
    if request.method == 'POST':
        form = ArticleBodyForm(request.POST, request.FILES, instance=article)
        if form.is_valid():
            form.save()
            
            return read_article(request,id)
    
    action = reverse('ajax_article_body_form', args=[id])
    form = ArticleBodyForm(instance=article)
    
    return render(request, 'ajaxform.html', {'form':form,'action':action})

    
        
   