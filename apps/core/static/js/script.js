// Images in enties scales down 
// in the entry. And scales up in 
// the dialog when clicked on.

var testvar;
                    
var preview_textarea = function(form, preview) {
        var data = form.serialize()+"&preview=" + preview;

        $.ajax( {
            type: "POST",
            url: '/utils/preview/',
            data: data,
            statusCode: {
                200: function( data ) {
                    console.log( data );
                    
                    var preview_modal = $('<div>'+data+'</div>');

                    preview_modal.dialog({
                        width: 800,
                        modal: true,
                        position: ['center',100],
                        title: 'Textförhandsgranskning',
                    });

                }
            }  
        });  
}

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
    // Annonce article notifications
    if ( data.a.ar != 0 ) {
        
        if ( data.a.ar == 1 ) {
            $.jGrowl( "Ny artikelkommentar" );
        
        } else if ( data.a.ar > 1 ) {
            $.jGrowl( String( data.a.ar ) + " nya artikelkommentarer" );
        }
    }
};

var update_indicators = function(data) {

    var window_indicator = 0;
    // Set guestbook indicator
    if ( data.i.gb != 0 ) {
        $('#gb-indicator').html("(" + data.i.gb + ")");    
        window_indicator += data.i.gb;
    } else {
        $('#gb-indicator').html("");
    }
    
    // Set forum indicator
    if ( data.i.fo != 0 ) {
        $('#fo-indicator').html("(" + data.i.fo + ")");
        window_indicator += data.i.fo;
    } else {
        $('#fo-indicator').html("");
    }    

    // Set article indicator
    if ( data.i.ar != 0 ) {
        $('#ar-indicator').html("(" + data.i.ar + ")");
        window_indicator += data.i.ar; 
    } else {
        $('#ar-indicator').html("");    
    }
    
    // Window title indicator
    if ( window_indicator != 0 ) {
        $('title').html('('+ window_indicator +') phx');
    } else {
        $('title').html('PHX');
    }
}




$(document).ready(function() {
    /*
    * Break out site from frames
    *
    */
    if (top != self) { top.location.replace(self.location.href); }

    /*
    * Edit entry button
    *
    */
    $('.js-entry-edit').button({
                            icons: {
                                primary: "ui-icon-pencil"
                            }
                        })
                        .click( function ( event ) {
                            event.preventDefault();
                            
                            var button = $( this ),
                                url = button.attr( 'href' ),
                                field = $( "#"+button.attr( 'rel' ) ),
                                initalHeight = field.height() + 100;
                                
                            // load form
                            field.load(  url , function () {
                                field.find('textarea').css( 'height' , initalHeight );
                            });

                            // change to save button
                            button.replaceWith( '  <a href="http://sv.wikipedia.org/wiki/Textile" class="js-help" target="_blank">Formateringshjälp</a><a href="'+ url +'" class="js-entry-save" rel="profile-description">Spara</a>');
                            $( '.js-entry-save' ).button({
                                icons: {
                                    primary: "ui-icon-pencil"
                                }
                            }).
                            click( function ( event ) {
                                
                                event.preventDefault();

                                $.ajax( {
                                    type: "POST",
                                    url: url,
                                    data: field.find('form').serialize(),
                                    statusCode: {
                                        200: function(data) {
                                            location.reload(true);
                                        }
                                    }
                                });
                            });
                            
                            $( '.js-help' ).button({
                                                  icons: {
                                                        primary: "ui-icon-help"
                                                    }
                            }).parent()
                                .buttonset();                            
                            return false;
                        });
                        
    /*
    * Ajaxforms
    *
    */
    $('.ajax-delete-note').submit( function (event) {
        event.preventDefault();
        
        form = $(this);

        $.ajax( {
            type: "POST",
            url: form.attr( 'action' ),
            data: form.serialize(),
            statusCode: {
                200: function() {
                    var anSelected = form.parents('tr');
                    $('#notification_table').dataTable( ).fnDeleteRow( anSelected[0] );

                    var number_of_notes = $('.ajax-delete-note').length;
                    $('#tab-counter-notes').html("(" + number_of_notes + ")");
                }
            }  
        });
        
        return false;
    });


    /*
    * Updates
    *
    */ 
                    
   // Auto updater
   var auto_update = setInterval( function () {
        $.ajax({
            data: get_data,
            contentType: "application/json; charset=utf-8",
            dataType: "json",
            url: "/notifications/updates.json",
            success: function(data){
                process_updates( data );
            },
            error: function(data) {
                console.log("Något fel har inträffat");
                console.log(data);
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
    
    
    /*
    * jQuery UI accordions
    *
    */
    
    $('.accordion').accordion({
        collapsible: true,
        active: false,
        autoHeight: false,         
    });
    
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
    

    /*
    * Preview button for textareas
    *
    */
    $('input:[data-preview]').click( function () {
        var form = $(this).parentsUntil('form').parent();
        var preview = $(this).data('preview');
        preview_textarea(form, preview);
    });

    // Show messages with jGrowl
    var messages = $('.jGrowlmessages li, .errorlist li');
    messages.hide();
    messages.each( function(){
        $.jGrowl(this.innerHTML);
    });
    
    // User jQuery datepicker
    $(".datePicker").datepicker({
            yearRange: "-100:+0",
            dateFormat: 'yy-mm-dd',
            defaultDate:'-25y',
            changeYear: true,
            changeMonth: true
            
        });


   // Hover username menu
   $('.link-user').mouseenter( function () {
        link = $(this);
        widget = link.parent('.ui-widget-header');
        menu = widget.next('ul.username-hover-menu');
        menu.fadeIn("fast");
   });
   
   $('ul.username-hover-menu').mouseleave( function () { 
        $(this).fadeOut("fast");
   });

   // Auto resize text areas 
   $('textarea').autoResize({
        // Quite slow animation:
        animateDuration : 300,
    });

});
