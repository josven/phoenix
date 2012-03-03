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
        $('title').html('('+ window_indicator +') PHX');
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
                                field.find('textarea').css( 'height' , initalHeight )
                                                      .autoResize({
                                                            // Quite slow animation:
                                                            animateDuration : 300,
                                                        });
                            });

                            // change to save button
                            button.replaceWith( '  <a href="http://sv.wikipedia.org/wiki/Textile" class="js-help" target="_blank">&nbsp;</a><a href="'+ url +'" class="js-entry-save" rel="profile-description">Spara</a>');
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
    * Delete entry button
    *
    */
    $('.js-entry-delete').button({
                            icons: {
                                primary: "ui-icon-trash"
                            }
                        })
                        .click( function ( event ) {
                            event.preventDefault();
                            
                            var button = $( this ),
                                url = button.attr( 'href' );
                                next_url = button.attr( 'data-next-url' );
                                
                            // load form
                            var dialog = $('<div></div')
                                .load( url )
                                .dialog({
                                    modal: true,
                                    title: "Radera?",
                                    buttons: {
                                        "Radera": function() {
                                            $.ajax( {
                                                type: "POST",
                                                url: url,
                                                data: $( this ).find('form').serialize(),
                                                statusCode: {
                                                    200: function(data) {
                                                        location.href = next_url;
                                                    },
                                                    428: function(data) {
                                                        console.log( dialog );
                                                        dialog.append('<p style="font-style:bold;">Du måste välja om du ska fortsätta</p>');
                                                    }
                                                }
                                            });
                                        },
                                        "Avbryt": function() {
                                            $( this ).dialog( "close" );
                                        }
                                    }
                                });
                           
                            return false;
                        });                        
   /*
    * History entry button
    *
    */
    $('.js-entry-history').button({
                            icons: {
                                primary: "ui-icon-folder-open"
                            }
                        })
                        .click( function ( event ) {
                            event.preventDefault();
                            
                            var button = $( this ),
                                url = button.attr( 'href' );
                                
                            // load form
                            var dialog = $('<div></div')
                                .load( url )
                                .dialog({
                                    modal: true,
                                    title: "Historik",
                                    width: $(window).width() - 50,
                                    height: $(window).height() - 150,
                                    buttons: {
                                        "Stäng": function() {
                                            $( this ).dialog( "close" );
                                        }
                                    }
                                });
                           
                            return false;
                        });
    /*
    * Convaseation entry button for guestbooks
    *
    */
    $('.js-entry-conversation').button({
                            icons: {
                                primary: "ui-icon-transferthick-e-w"
                            }
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
    /*
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
    */
    
    // Checkboxtags are toggleble tag buttons. Used when new entry are created.
    $('.ui-tag-edit input[type=checkbox]').button( {icons: {primary:'ui-icon-pencil'}});
    
    //$('.ui-tag input[type=checkbox]').button( {icons: {primary:'ui-icon-tag'}});

    
    
    /*
    * Entrys
    *
    */
    formatImageDialogs();
    
    // Linktags, with toggable subcribe buttons.
    $.each( $('.ui-tag-link'), function () {
        
        var tag = $(this),
            toggle = tag.find('.ui-tag-link-toggle'),
            toggle_icon = toggle.attr('data-icon'),
            toggle_form = tag.find('.ui-tag-link-form'),
            toggle_url = toggle_form.attr('action');
            
        toggle.button({ 
            icons: {primary: toggle_icon },
            text: false,
        })
        .click(function(event) {
            event.preventDefault();
            
            $.ajax( {
                type: "POST",
                url: toggle_url,
                data: toggle_form.serialize(),
                statusCode: {
                    200: function(data) {
                        $.jGrowl(data.message);
                        if ( data.tag_status == 1 ) {
                            $('.ui-tag-link-toggle[rel="'+toggle.attr('rel')+'"]').button("option", "icons", { primary: 'ui-icon-star' });
                            
                            
                        } else if(data.tag_status == 0) {
                            $('.ui-tag-link-toggle[rel="'+toggle.attr('rel')+'"]').button("option", "icons", { primary: 'ui-icon-tag' });
                        }
                        
                    }
                }
            
            });
            
        return false;    
        
		}).next().button().parent().buttonset();
        
    });

    
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

   // Auto resize text areas 
   $('textarea').autoResize({
        // Quite slow animation:
        animateDuration : 300,
    });

    // Apply jQuery UI on pagination
    $('.pagination').buttonset();
    $('.pagination .disabled').button({ disabled: true });
    $('.pagination .current').button().addClass('ui-state-active');
    $('.pagination .elips').button();
    
});