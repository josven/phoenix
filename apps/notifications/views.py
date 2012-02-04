# -*- coding: utf-8 -*-

from django.http import HttpResponse
from django.utils import simplejson

from django.views.decorators.cache import never_cache
from django.contrib.auth.decorators import login_required

from apps.notifications.models import *
from django.http import HttpResponseRedirect  
from apps.core.utils import render

NOTIFICATION_TYPES = (
    (1, 'Gästboksinlägg'),
    (2, 'Forumsvar'),
    (3, 'Artikelkommentar'),
)

@never_cache
@login_required(login_url='/auth/login/')
def delete_notification(request):
    
    vars = {}
    
    if request.method == 'POST':
            
        notification_id = request.POST.get('notification_id', None)     
        instance_id = request.POST.get('instance_id', None)                 
        type = request.POST.get('type', None)
        
        if notification_id:      
            notification = Notification.objects.get(receiver=request.user,id=notification_id)       
            if notification:
                notification.delete()      

        elif instance_id and type:
            notification = Notification.objects.get(receiver=request.user, instance_id=instance_id, type=type)        
            if notification:
                notification.delete()      

    return HttpResponseRedirect(request.META["HTTP_REFERER"]) 

@never_cache
@login_required(login_url='/auth/login/')
def updates(request, format):
    
    if request.is_ajax():
        if request.user.is_authenticated():
            data = get_notifications(request)
            
            if format == 'xml':
                mimetype = 'application/xml; charset=utf8'
                
            if format == 'json':
                mimetype = 'application/javascript; charset=utf8'
            
            json_data = simplejson.dumps( data )
 
        return HttpResponse(json_data,mimetype)
   
    else:
    
        return HttpResponse(status=400)       
    

def get_notifications(request):
    
    d = {}
    user = request.user
    notifications = Notification.objects.filter(receiver=user)
    
    count_new_guestbook = 0
    count_indicator_guestbook = 0

    count_new_forum = 0
    count_indicator_forum = 0

    count_new_article = 0
    count_indicator_article = 0
        
    if notifications:
        
        for notification in notifications:
        
            # Get new guestbook annuoucements
            if ( notification.instance_type == "Guestbooks" ) & ( int( float( notification.status ) ) == 1 ):
                count_new_guestbook += 1
                notification.status = 2
                notification.save()
            
            # Get guestbook indicator       
            if ( notification.instance_type == "Guestbooks" ) & ( int( float( notification.status ) ) < 4 ):
                count_indicator_guestbook += 1    
                
            # Get new forum annuoucements            
            if ( notification.instance_type == 'ForumComment' ) & ( int( float( notification.status ) ) == 1 ):
                count_new_forum += 1
                notification.status = 2
                notification.save()
            
            # Get forum indicator       
            if ( notification.instance_type == 'ForumComment' ) & ( int( float( notification.status ) ) < 4 ):
                count_indicator_forum += 1  
                              
            # Get new article annuoucements            
            if ( notification.instance_type == 'ArticleComment' ) & ( int( float( notification.status ) ) == 1 ):
                count_new_article += 1
                notification.status = 2
                notification.save()
            
            # Get forum indicator       
            if ( notification.instance_type == 'ArticleComment' ) & ( int( float( notification.status ) ) < 4 ):
                count_indicator_article += 1
        
    d = { 'a' : { 'gb' : count_new_guestbook, 'fo' : count_new_forum , 'ar' : count_new_article }, 'i' : { 'gb' : count_indicator_guestbook, 'fo' : count_indicator_forum, 'ar' : count_indicator_article } }
     
    return d

    
@never_cache
@login_required(login_url='/auth/login/')    
def notifications(request):
    vars ={}
    
    notifications = Notification.objects.filter(receiver=request.user)

    vars['notifications'] = notifications
    
    return render(request, "notifications.html", vars )
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    

    
    
    
    
    
'''
        for status in STATUS_CHOICES:
            
            
            
            for type in NOTIFICATION_TYPES:
                
                
                for notification in notifications:
                        
                        #print d['a'][ 't' ][ str( type[0] ) ][ str( status[0] ) ]['amount'] += 1
                        
                        
                        # Announcemets
                        
                        if notification.status == 1:
                            #updates_dict['a'][ str( status ) ][ str( type )]['text'] = "nonsens"
                            d['a'][ 't' ][ str( type[0] ) ][ str( status[0] ) ]['amount'] += 1
                        
                        
                        
                        # Indicators
                        if notification.status < 4:
                            updates_dict['i'][ str( status ) ][ str( type )]['text'] = "nonsen igen"
                            d['i'][ 't' ][ str( type[0] ) ][ str( status[0] ) ]['amount'] += 1


            for type in NOTIFICATION_TYPES:
                
                type_dict = {}
                
                
                for notification in notifications:
                    
                    
                    
                    # Only annonce new notification
                    if notification.status == 1: #NEW
                        
                        if int( float( notification.type[0] ) ) == int( float ( type[0] ) ):                              
                            print "New {0} status {1}".format( notification.type, notification.status )
                            
                            type_dict[ str( type[0] ) ]['a'].append( notification )

                            # Set status on the notification to annonced
                            notification.status = 2
                            notification.save()
                    
                    # alert noteicationns, used for counters in the menubar
                    if notification.status < 4: #All notifications exect for unreplied
                        
                        if int( float( notification.type[0] ) ) == int( float ( type[0] ) ):  
                            print "Status alert: {0} status {1}".format( notification.type, notification.status )
                            
                            
                    
                amount_of_messages =  len( typearray )
                
                # if only one note of that type
                if amount_of_messages == 1:
                    messages_dict[str (type[0])] = {'number': 1, 'text': notification.message}
                        
                # If more then one note in that type, collect them in one message
                elif amount_of_messages > 1:
                    messages_dict[str (type[0])] = {'number': amount_of_messages, 'text': "Nytt! {0} {1}".format( amount_of_messages, type[1] )}
                
    #return "TEST"
        
'''




