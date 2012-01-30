// Images in enties scales down 
// in the entry. And scales up in 
// the dialog when clicked on.

var testvar;
                    
var formatImageDialogs = function() {
    $('.entry-content img, .ui-text-panel img')
        .attr('height','80')
        .unbind('click')
        .click( function () {
            $(this).clone().dialog({ 
                                    resizable: false,
                                    modal: true,
                                    width:'auto'
                                    });
            });
}

var formatJsReplyButton = function() {
    $('.js-reply').button({
        icons: {
            primary: "ui-icon-comment"
        },
        text: false
    });
};


// Data to catch
var get_data = {
                "n": true,
                };
                
// process all new updates
var process_updates = function(data) {
  
    // Display new notifications 
    update_notifications(data);
    
    // Display indicators
    update_indicators(data);
}


var update_notifications = function(data) {

    // Annonce guestbook notifications
    if ( data.a.gb != 0 ) {
        
        if ( data.a.gb == 1 ) {
            $.jGrowl( "Nytt gästboksinlägg" );
        
        } else if ( data.a.gb > 1 ) {
            $.jGrowl( String( data.a.gb ) + " nya gästboksinlägg" );
        }
    }
    // Annonce forum notifications
    if ( data.a.fo != 0 ) {
        
        if ( data.a.fo == 1 ) {
            $.jGrowl( "Nytt svar i forumet" );
        
        } else if ( data.a.fo > 1 ) {
            $.jGrowl( String( data.a.fo ) + " nya svar i forumet" );
        }
    }
};

var update_indicators = function(data) {

    // Set guestbook indicator
    if ( data.i.gb != 0 ) {
        if ( data.i.gb > 0 ) {
            $('#gb-indicator').html(data.i.gb);    
        }
    }
    // Set guestbook indicator
    if ( data.i.fc != 0 ) {
        if ( data.i.fc > 0 ) {
            $('#fc-indicator').html(data.i.fc);    
        }
    }
}

var update_chat = function(data) {
    
    

}

$(document).ready(function() {
     
    /*
    * Break out site from frames
    *
    */
    if (top.location != self.location) {
        top.location = self.location;
    }

    /*
    * Updates
    *
    */ 
                    
   // Auto updater
   var auto_update = setInterval(
    
    function ()
    {
        $.ajax({
            data: get_data,
            contentType: "application/json; charset=utf-8",
            dataType: "json",
            url: "/notifications/updates.json",
            success: function(data){
                process_updates( data );
            },
            error: function() {
                $.jGrowl("Något fel har inträffat");
            }
        });
        
    }, 30000); // refresh every 30000 milliseconds

    

    
    /*
    * Polyfills
    *
    */
    
    // Placeholder
    $('input, textarea').placeholder();
    
    
    /*
    * Tags
    * 
    */
    
    // HACK until we have real widgets based on CheckboxSelectMultiple for tags 
    $('input[type=checkbox].ui-tag-reformat').parent('label').each( function() {
        var label = $(this),
            input = label.find('input'),
            tag = input.val();
        
        // Format label
        label.html( tag.charAt(0).toUpperCase() + tag.substr(1).toLowerCase() );
        
        // Insert input before label
        label.before( input );
        
        // Add class to parent
        label.parent().addClass('ui-tag');
 
        // Remove class on input
        input.removeClass('ui-tag');
    });
    
    // Checkboxtags are toggleble tag buttons. Used when new entry are created.
    $('.ui-tag-edit input[type=checkbox]').button( {icons: {primary:'ui-icon-pencil'}});
    
    $('.ui-tag input[type=checkbox]').button( {icons: {primary:'ui-icon-tag'}});

    
    
    /*
    * Entrys
    *
    */
    formatImageDialogs();
    
    // Linktags, these tags are links, simply put.
    $('.ui-tag a').button( { icons: {primary:'ui-icon-tag'}} );
    
    
    // Apply jQuery UI buttons
    $( "input:submit, a.ui-button, button").button();
    $( ".buttonset" ).buttonset();

    formatJsReplyButton();

    $( "#account_button" )
			.button()
            
			.next()
				.button( {
					text: false,
					icons: {
						primary: "ui-icon-gear"
					}
				})
				.click(function() {
					//alert( "Visa inställningar" );
				})
				.parent()
					.buttonset();
            
       
    });
    
    // Show messages with jGrowl
    var messages = $('.jGrowlmessages li, .errorlist li');
    messages.hide();
    messages.each( function(){
        $.jGrowl(this.innerHTML);
    });
    
    // User jQuery datepicker
    $(".datePicker").datepicker({dateFormat: 'yy-mm-dd', defaultDate:'-25y',  changeYear: true, changeMonth: true });


   // Hover username menu
   $('.link-user').mouseenter( function () {
        link = $(this);
        widget = link.parent('.ui-widget-header');
        menu = widget.next('ul.username-hover-menu');
        console.log(menu);
        
        menu.fadeIn("fast");
   });
   
   $('ul.username-hover-menu').mouseleave( function () {
        
        $(this).fadeOut("fast");
   });






