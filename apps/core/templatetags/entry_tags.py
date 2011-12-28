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
def entry_foot(entry):
    """
    Template tag for writing out head of entrys/post
    
    """
    
    output = "<div class=\"buttonset\">  \
                <a href=\"#\" class=\"ui-button ui-button-reply ui-corner-left\">Svara</a>  \
                <a href=\"#\" class=\"ui-button ui-button-mail \">Mail</a>  \
                <a href=\"#\" class=\"ui-button ui-button-guestbook \">Gästbok</a>  \
              </div>"
    
    return output