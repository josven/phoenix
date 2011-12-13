from django import template

register = template.Library()

@register.simple_tag
def entry_head(entry):
    """
    Template tag for writing out head of entrys/post
    
    """
    
    output ="<h4><a class=\"link-user\" href=\"/user/" + str( entry.created_by.id ) + "\">" + str( entry.created_by ) + "</a> - <em>" + str( entry.date_created ) + "</em></h4>"

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