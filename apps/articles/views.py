# -*- coding: utf-8 -*-
from models import *
from forms import *
from django.contrib import messages
from django.contrib.auth.models import User, Group
from django.contrib.auth.decorators import login_required, permission_required
from django.views.decorators.cache import never_cache
from django.http import Http404, HttpResponseRedirect
from apps.core.utils import render, validate_internal_tags
from django.core.urlresolvers import reverse

"""
Articles

"""

@never_cache
@login_required(login_url='/auth/login/')
def create_article(request, tags=None):
    """
    Create article
    
    """
    
    vars = {
        'form':ArticleForm(),
        'tagform' : DefaultArticleTagsForm(),
        'categories':defaultArticleCategories.objects.all(),
        'moderator_categories': ModeratorArticleCategories.objects.all(),
        }
    
    if tags != None:
        initial_tags = tags.split(',')
        vars['tagform'] = DefaultForumTagsForm(initial={'default_tags': initial_tags })
        
    if request.method == 'POST':
        form = ArticleForm(request.POST)
        tagform = DefaultArticleTagsForm(request.POST)
        
        vars['form'] = form
        vars['tagform'] = tagform
        
        if form.is_valid() & tagform.is_valid():
            default_tags = tagform.cleaned_data['default_tags']
            user_tags = form.cleaned_data['tags']
            
            # Combine and remove doubles
            all_tags = list(set(default_tags + user_tags))
            
            # Check if a default tag is present
            if len(default_tags) == 0:
                messages.add_message(request, messages.INFO, 'Du måste välja minst en huvudkategori!')
                return render(request,'create_article.html', vars)

            # Check maximum allowed tags
            if len( all_tags ) > 5:
                messages.add_message(request, messages.INFO, 'Du kan inte välja fler än fem kategorier!')
                return render(request,'create_article.html', vars)

            post_values = request.POST.copy()
            all_tags = validate_internal_tags(request, all_tags)
            post_values['tags'] = ', '.join(all_tags)
            
            try:
                if post_values['allow_comments'] == "on":
                    post_values['allow_comments'] = True
            except:
                post_values['allow_comments'] = False
                
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
def read_article(request,user_id=None, id=None):
    """
    Read article
    
    """
    print "läs"
    
    vars = {
        'categories': defaultArticleCategories.objects.all(),
        'ArticleBodyForm': ArticleCommentForm(),
        }
    
    if id==None:
        """
        return all articles
        """
        vars['articles'] = Article.objects.all()
        
        return render(request,'articles.html', vars)
    
    vars['article'] = Article.objects.get(id=id)
    vars['comments'] = ArticleComment.objects.filter(post=vars['article'])

    if user_id:
        template = "user_article.html"
        vars['user'] = User.objects.get(pk=user_id)
    else:
        template = "article.html"
           
    return render(request,template, vars)

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

    tags = [x for x in tags.split(",")]
    
    if user_id and tags:
        articles = Article.active.filter(tags__name__in=tags, created_by__id = user_id)
        template = 'user_articles.html'
    else:
        template = 'articles.html'
    
    if tags and not user_id:
        articles = Article.active.filter(tags__name__in=tags)
    else:
        Article.active.all()
        
    if len( articles ) < 1:
        messages.add_message(request, messages.INFO, 'Hittade inga artiklar =(')
    
    vars = {"articles": articles,
            "categories":categories
            }
    if user_id:
        vars['user'] = User.objects.get(pk=user_id)
    
    return render(request, template, vars)
    
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

    
       
@never_cache
@login_required(login_url='/auth/login/')
def comment_article(request,article_id):
    """
    Comment article
    
    """
    
    post = Article.objects.get(id=article_id)
    
    
    vars = {
        
    }
    
    if request.method == 'POST':
        author = request.user
        form = ArticleCommentForm(request.POST)
        
        if form.is_valid(): 
            comment = ArticleComment(
                post = post,
                created_by = request.user,
                author=author,
                comment=request.POST['comment'],
            )
            
            # if this is a reply to a comment, not to a post
            if request.POST['parent_id'] != '':
                comment.parent = ArticleComment.objects.get(id=request.POST['parent_id'])
            comment.save()
 
    return HttpResponseRedirect(reverse('read_article', args=[article_id]))