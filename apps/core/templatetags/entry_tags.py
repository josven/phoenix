# -*- coding: utf-8 -*-

from django import template
from django.core.urlresolvers import reverse





from apps.core.utils import find_request

register = template.Library()







from django.contrib.humanize.templatetags.humanize import naturalday
from apps.core.templatetags.filters import user_filter

@register.inclusion_tag('entry_template.html')
def render_entry(entry, request=None):
  
    vars = {
        'id':entry.id,
        'author':entry.created_by,
        'reply_url':getattr(entry,'get_reply_url', None)
        }

    # Get notifications
    notifications = getattr(request,'notifications',None)
    if notifications:
        # Find notification on entry
        for note in notifications:          
            if note.instance_type == entry.__class__.__name__ and note.instance_id == entry.id:
                vars['note'] = note

    # Get date
    date_names = ['date_created', 'added']
    date_value = _get_first_valid_value(entry, date_names)
    vars['date'] = u"{0} {1}".format( naturalday( date_value[1]), date_value[1].strftime("%H:%M") )
        
    # Get title
    title_names = ['title']
    title_value = _get_first_valid_value(entry, title_names)
    if title_value:
        vars['title'] = title_value[1]
    
    # Get tags 
    tags_attr = getattr(entry, 'tags', None)
    if tags_attr:
        vars['tags'] =  tags_attr.all()
    
    # Find content
    content_names = ['body', 'comment','text']
    content_value = _get_first_valid_value(entry, content_names)
    vars['content'] = content_value[1]
    vars['reply_textarea'] = content_value[0]
    
    # Reply button if comment
    if getattr(entry, 'comment', None):
        vars['reply_button'] = True

    # Reply button if chatpost
    if entry.__class__.__name__ == "Post":
        vars['reply_button'] = True
    
    # Reply button for guestbook
    if entry.__class__.__name__ == "Guestbooks" and request.user != vars['author']:
        vars['reply_button'] = True
    
    # if is_editable
    if getattr(entry,'ajax_editable_fields',False) and vars['author'] == request.user:
        vars['is_editable'] = getattr(entry, 'is_editable', None)
        vars['update_url'] = reverse('update_entry', args=[entry._meta.app_label, entry.__class__.__name__, entry.id])

    # if deleteble
    if vars['author'] == request.user:
        vars['is_deleteble'] = getattr(entry, 'is_deleteble', None)
        vars['delete_url'] = reverse('delete_entry', args=[entry._meta.app_label, entry.__class__.__name__, entry.id])
        vars['delete_next_url'] = getattr(entry, 'delete_next_url', None)
        
    # if history
    
    if getattr(entry,'last_changed_by',False) and getattr(entry,'entry.allow_history', False):
        vars['history_url'] = reverse('history_entry', args=[entry._meta.app_label, entry.__class__.__name__, entry.id])
    
    return vars

@register.inclusion_tag('userlink_template.html')
def render_userlink(user):
    vars = {
        'username':user.username,
        'id':user.id
        }
        
    return vars   
    
@register.inclusion_tag('tag_template.html')
def render_tag(tag):
    vars = {
        'tag':tag,
        }
        
    return vars

def _get_first_valid_value(obj, keys):
    
    values = dict((name, getattr(obj, name, None)) for name in keys)

    for item in values.items():      
        if item[1]:      
            return item
    
    return None








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
    
    
    

class AssignNode(template.Node):
    def __init__(self, name, value):
        self.name = name
        self.value = value
        
    def render(self, context):
        context[self.name] = self.value.resolve(context, True)
        return ''

@register.filter 
def endlist(value, arg):
    jumps =  abs(int(float(value)) - int(float(arg)))
    return " ".join( ["</ul><!-- GENERATED number{0} of {1} -->".format(count, jumps)  for count in range(0,jumps)] )

@register.filter 
def jumpdowns(value, arg):
    jumps =  abs(int(float(value)) - int(float(arg)))
    return ["<h3>jumpdown!</h3>" for count in range(0,jumps)]

    
@register.tag   
def do_assign(parser, token):
    """
    Assign an expression to a variable in the current context.
    
    Syntax::
        {% assign [name] [value] %}
    Example::
        {% assign list entry.get_related %}
        
    """
    bits = token.contents.split()
    if len(bits) != 3:
        raise template.TemplateSyntaxError("'%s' tag takes two arguments" % bits[0])
    value = parser.compile_filter(bits[2])
    return AssignNode(bits[1], value)