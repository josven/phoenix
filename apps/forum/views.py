# -*- coding: utf-8 -*-
import re
import copy


import json
from django.http import HttpResponse
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User, Group
from django.contrib import messages
from django.http import Http404, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.views.decorators.cache import never_cache
from apps.core.utils import render, validate_internal_tags, get_datatables_records
from models import *
from forms import *

from apps.notifications.models import Notification

''' New forum '''


@never_cache
@login_required()
def list_forum_json(request, tags=None):

    if request.is_ajax():

        #initial querySet
        if tags:
            tags_array = tags.split(",")
            querySet = Forum.active.filter(tags__name__in=tags_array)
        else:          
            querySet = Forum.active.all()
        
        if not request.user.has_perm('forum.access_mod_forum'):
            querySet = querySet.exclude(tags__name="MOD")
        
        #columnIndexNameMap is required for correct sorting behavior
        columnIndexNameMap = { 
                                0: 'title',
                                1: 'tags',
                                2: 'date_created',
                                3: 'id',
                                4: 'posts_index',
                                5: 'last_comment__id',
                                6: 'last_comment__id',
                            }

        #call to generic function from utils
        return get_datatables_records(request, querySet, columnIndexNameMap)

    raise Http404 


@never_cache
@login_required()
def list_forum(request, tags=None):

    """
    List of forum threads.
    
    """

    vars = {
        "categories":defaultCategories.objects.all(),
        }

    if request.user.has_perm('forum.access_mod_forum'):
        mod_tag = ModeratorForumCategories.objects.filter(tags__name__in=["MOD"])
        vars["categories"] = list( vars["categories"] ) + list( mod_tag )
        
    if tags:
        tags_array = tags.split(",")
        vars['tags'] = tags

    return render(request, 'list_forum.html', vars )



@never_cache
@login_required()
def read_forum(request, id, comment_id = None):

    vars = {
        'categories' : defaultCategories.objects.all(),
        'commentform' : ForumCommentForm(),
        'article_id' : id,
        'article' : Forum.objects.get(id=id),
        }


    if "MOD" in [tag.name for tag in vars['article'].tags.all()]:
        if not request.user.has_perm('forum.access_mod_forum'):
            raise Http404

    try:
        forum_note = request.user.receiver_entries.get(content_type__model = 'forum', object_id = id)
    except:
        forum_note = None
    
    if forum_note:
        forum_note.delete()


    ## Kommentar notifikationer
    ##--------------------------
    
    if comment_id != None:
        comments = ForumComment.objects.filter(id = comment_id)
    else:
        comments = ForumComment.objects.filter(post=vars['article'])

    comments = list( comments )
    
    vars['comments'] = comments
    
    return render(request, 'read_forum.html', vars )


@never_cache
@login_required()
def create_forum(request, tags=None):

    if tags:
        initial_tags = tags.split(',')
        tagform = DefaultForumTagsForm(initial={'default_tags': initial_tags })
    else:
        tagform = DefaultForumTagsForm()

        
    vars = {
            'form' : ForumForm( user=request.user ),
            'tagform' : tagform,
            'categories' : defaultCategories.objects.all(),
        }
        
    if request.method == 'POST':    
        form = ForumForm(request.POST, user=request.user)
        tagform = DefaultForumTagsForm(request.POST)

        if form.is_valid() & tagform.is_valid():        
            default_tags = tagform.cleaned_data['default_tags']
            
            user_tags = form.cleaned_data['tags']
            user_sub_tags = form.cleaned_data['user_tags']

            # Filter list from empty strings
            cleaned_tags = filter(None, user_tags)
            
            # Combine and remove doubles
            all_tags = list(set(default_tags + cleaned_tags + user_sub_tags))
                
            # Check if a default tag is present
            if len(default_tags) == 0:
                messages.add_message(request, messages.INFO, 'Du måste välja minst en huvudkategori!')
                return render(request, 'create_forum.html', {'form': form,'tagform':tagform, 'categories':vars['categories']})

            # Check maximum allowed tags
            if len( all_tags ) > 5:
                messages.add_message(request, messages.INFO, 'Du kan inte välja fler än fem kategorier!')
                return render(request, 'create_forum.html', {'form': form,'tagform':tagform, 'categories':vars['categories']})
            
            post_values = request.POST.copy()

            # Validate INTERNAL tags
            all_tags = validate_internal_tags(request, all_tags)
            post_values['tags'] = ', '.join(all_tags)
            
            form = ForumForm(post_values, user=request.user)  
            link = form.save()

            return HttpResponseRedirect(reverse('read_forum', args=[link.id]))

    return render(request, 'create_forum.html', vars )


@never_cache
@login_required()
def comment_forum(request,forum_id):
    """
    Comment article
    
    """
    
    post = Forum.objects.get(id=forum_id)
    
    vars = {
        
    }
    
    if request.method == 'POST':
        author = request.user
        form = ForumCommentForm(request.POST)
        
        if form.is_valid(): 
            comment = ForumComment(
                post = post,
                created_by = request.user,
                author=author,
                comment=request.POST['comment'],
            )
            
            
            # if this is a reply to a comment, not to a post
            if request.POST['parent_id'] != '':
                comment.parent = ForumComment.objects.get(id=request.POST['parent_id'])
            
            # Save comment
            comment.save()
            

            # Get instance ids for all siblings
            # if there are any unreplied siblings we need to remove them
            instance_ids = []
            if comment.is_child_node():              
                try:
                    siblings = comment.get_siblings(include_self=False)
                    instance_ids = [sibling.id for sibling in siblings]
                except:
                    pass

            # Put parent post in to the array
            if comment.parent:
                instance_ids += [comment.parent.id]

            # Get notifications and remove them all
            notifications = request.user.receiver_entries.filter(content_type__model = 'forumcomment', object_id__in = instance_ids)

            if notifications:
                for note in notifications:
                    note.delete()

            post.last_comment = comment
            
            if post.posts_index:
                post.posts_index  += 1
            else:
                post.posts_index = post.get_posts_index()
                
            post.save()
            
            ## Kommentar notifikationer
            ##--------------------------

            comments = ForumComment.objects.filter(post=post)
            comments = list( comments )
            comments_ids = [comment.id for comment in comments]

            # Tar upp notifikationer för kommentarer
            notifications = request.user.receiver_entries.filter(content_type__model = 'forumcomment', object_id__in = comments_ids)

            for notification in notifications:
                for comment in comments:
                    if comment.id == notification.object_id:

                        # Hänger på notifikationen på kommentaren
                        comment.notification = notification

                        # Eftersom komentaren är nu läst så sätter vi status 3 på den (obesvarad)
                        notification.status = 3
                        notification.save()

            if request.is_ajax():
                vars = {
                    'comments' : comments,
                    'article_id': forum_id,
                    'commentform': ForumCommentForm(),
                    'app_name': "forum",
                    'model_name': "ForumComment",
                    'post_url': reverse('comment_forum', args=[forum_id]),
                    }

            return render(request, '_comments.html', vars )
    
    return HttpResponseRedirect(reverse('read_forum', args=[forum_id]))

''' ######################## old forum ############################ '''

@never_cache
@login_required()
def read_old_forum(request):
    """
    Read the list of forum threads.
    
    """

    categories = defaultCategories.objects.all()
    threads = Thread.active.all()
  
    vars = {
            "threads": threads,
            "categories":categories
            }

    return render(request, 'old_forum.html', vars )

@never_cache
@login_required()
def create_thread(request, tags=None):
    """
    Create a forum thread.
    
    """

    threads = Thread.active.all()
    form = ThreadForm()
    tagform = DefaultForumTagsForm()
    categories = defaultCategories.objects.all()
    
    if tags != None:
        initial_tags = tags.split(',')
        tagform = DefaultForumTagsForm(initial={'default_tags': initial_tags })
    
    if request.method == 'POST':    
        form = ThreadForm(request.POST)
        tagform = DefaultForumTagsForm(request.POST)
        
        if form.is_valid() & tagform.is_valid():            
            default_tags = tagform.cleaned_data['default_tags']
            
            user_tags = form.cleaned_data['tags']
                       
            # Filter list from empty strings
            cleaned_tags = filter(None, user_tags)
            
            # Combine and remove doubles
            all_tags = list(set(default_tags + cleaned_tags))
                
            # Check if a default tag is present
            if len(default_tags) == 0:
                messages.add_message(request, messages.INFO, 'Du måste välja minst en huvudkategori!')
                return render(request, 'create_thread.html', {"threads": threads, 'form': form,'tagform':tagform, 'categories':categories})

            # Check maximum allowed tags
            if len( all_tags ) > 5:
                messages.add_message(request, messages.INFO, 'Du kan inte välja fler än fem kategorier!')
                return render(request, 'create_thread.html', {"threads": threads, 'form': form,'tagform':tagform, 'categories':categories})

            # Validate INTERNAL tags
            all_tags = validate_internal_tags(request, all_tags) 
            
            # Create the thread
            thread = Thread.objects.create(
                created_by = request.user,
                title = form.cleaned_data['title']
            ) 
            
            # Apply tags on thread
            for tag in all_tags:
                thread.tags.add(tag)  
            
            # Create the initial post
            ForumPost.objects.create(
                created_by=request.user,
                collection=thread,
                body=form.cleaned_data['body']
            )
            
            return HttpResponseRedirect(thread.get_absolute_url())

    return render(request, 'create_thread.html', {"threads": threads, 'form': form,'tagform':tagform, 'categories':categories})

@never_cache
@login_required()
def read_thread(request, id):
    """
    Read a forum thread.
    
    """
    categories = defaultCategories.objects.all()
    
    try:
        thread = Thread.active.get(id=id)
    except:
        raise Http404

    posts =  ForumPost.objects.decorated(collection=thread, deleted_by=None)

    data = {
        'thread': thread,
        'posts': posts, 
        'form': ForumPostForm(), 
        'categories':categories
        }
        
    return render(request, 'thread.html', data)

@never_cache
@login_required()
def create_forumpost(request, tags=None):
    """
    Create a forumpost. FormPost class will handle all threading logic.
    
    """
    form = ForumPostForm(request.POST)
    if form.is_valid():
        try:
            thread = Thread.active.get(id=form.cleaned_data['thread_id'])
        except:
            raise Http404

        save_method = request.POST['save_method']
        
        # If the parent does not equal the given thread, abort!
        if 'parent_id' in form.cleaned_data and form.cleaned_data['parent_id']:
            try:
                parent = ForumPost.objects.get(id=form.cleaned_data['parent_id'])
            except:
                raise Http404
            if parent.collection != thread:
                raise Http404

        # Create the post
        post = ForumPost(
            parent_id=form.cleaned_data['parent_id'],
            created_by=request.user,
            collection=thread,
            body=form.cleaned_data['body'],
        )
        
        # Overide the save method
        if save_method:
            post.save(save_method=save_method)
        
        return HttpResponseRedirect(thread.get_absolute_url())

    try:
        thread = Thread.active.get(id=request.POST['thread_id'])
    except:
        raise Http404
    posts = ForumPost.objects.decorated(collection=thread)
    form = ForumPostForm()

    data = {"thread": thread, 'posts': posts, 'form': form}
    return render(request, 'thread.html', data)

@never_cache
@login_required()
def get_threads_by_tags(request,tags):
    categories = defaultCategories.objects.all()
    tags_array = tags.split(",")
    threads = Thread.active.filter(tags__name__in=tags_array)
    
    if len( threads ) < 1:
        messages.add_message(request, messages.INFO, 'Hittade inga trådar =(')

    return render(request, 'old_forum.html', {"threads": threads,"categories":categories,"tags":tags})