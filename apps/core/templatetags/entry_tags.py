# -*- coding: utf-8 -*-

from django import template
from django.core.urlresolvers import reverse
from apps.core.utils import find_request

register = template.Library()

@register.simple_tag
def entry_head(entry):
    """
    Template tag for writing out head of entrys/post
    
    """
    request = find_request()
    appname = request.session['app_name']
    
    output ="<h4 class=\"ui-widget-header entry-head\"> \
                <a class=\"link-user\" href=\"" + reverse('read_profile', args=[ entry.created_by.id ]) + "\"> \
                    " + str( entry.created_by ) + " \
                </a> - <em>" + str( entry.date_created ) + "</em>"
            
    output += "<div class=\"button-wrapper\">"

    if request.user != entry.created_by or appname == "forum":
        output += "<a href=\"#\" data-reply-to=\"" + str( entry.created_by ) + "\" class=\"js-reply\">Svara</a>"
    output += "</div>"
    
    output += "</h4>"

    output += "<ul class=\"username-hover-menu ui-helper-hidden ui-widget ui-widget-content\"> \
                <li><a href=\"" + reverse('read_profile', args=[entry.created_by.id]) + "\">Profil</a></li> \
                <li><a href=\"" + reverse('guestbook', args=[entry.created_by.id]) + "\">Gästbok</a></li> \
              </ul>"

    return output

@register.simple_tag    
def thread_header(entry):
    """
    Template tag for writing out header of entrys/post
    Based on the first post.
    
    """
    
    title = unicode( entry.collection.title )
    tags = entry.collection.tags.all()
        
    tags = u' '.join([ "<span class=\"ui-tag\"><a href=\"" + reverse('get_threads_by_tags', args=[tag]) + "\">" + unicode( tag ).title() + "</a></span>" for tag in tags ])
    
    html = u"<h4 class=\"ui-widget-header entry-head\">{0} &nbsp; {1} </h4>".format( title , tags )
    
    return html
    
@register.simple_tag    
def article_header(entry):
    """
    Template tag for writing out header of articles
    
    """
    
    title = entry.title
    tags = entry.tags.all()
    
    tags = u' '.join([ "<span class=\"ui-tag\"><a href=\"" + reverse('search_article', args=[tag]) + "\">" + unicode( tag ).title() + "</a></span>" for tag in tags ])
    
    html = u"<h4 class=\"ui-widget-header entry-head\">{0} av {1} den {2} {3} </h4>".format( unicode( title ), unicode( entry.created_by ), unicode( entry.date_created ), unicode( tags ) )
    
    return html