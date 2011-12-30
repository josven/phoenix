testvar = {}

$(document).ready(function() {

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
    
    /*
        .click( function () {
            var entry = $(this).parentsUntil('ul').last(),
                form = entry.find('form');
            
            // hide 
            console.log( entry );
            console.log( form );
        });
    */
    
    $('.ui-tag input[type=checkbox]').button( {icons: {primary:'ui-icon-tag'}});
    
    /*
        .click( function () {
            var button = $(this),
                tag = button.data('tag');
            
            // Hilight button
            button.toggleClass('ui-state-active');
            
            // Populate tagholder
            var tagholder = $( "#id_tags" );
            if ( tagholder.length != 0 ) {
                var tags = ""; //= tagholder.innerHTML;
                $('.ui-tag input[type=checkbox].ui-state-active').each( function () {
                    tags = tags + " " + $(this).data('tag');
                });
                tagholder.val( tags.trim() );
            }
        });
    */
    
    
    /*
    * Entrys
    *
    */
    // Images in enties scales down 
    // in the entry. And scales up in 
    // the dialog when clicked on.
    $('.entry-content img, .ui-text-panel img')
        .attr('height','80')
        .click( function () {
            $(this).clone().dialog({ 
                                    resizable: false,
                                    modal: true,
                                    width:'auto'
                                    });
        });
    
    // Activate initial active tags
    //$('input[type=checkbox].ui-tag-init-active').toggleClass('ui-state-active');
    
    // Linktags, these tags are links, simply put.
    $('.ui-tag a').button( { icons: {primary:'ui-icon-tag'}} );
    
    
    
    
    // Apply jQuery UI buttons
    $( "input:submit, a.ui-button, button").button();
    $( ".buttonset" ).buttonset();

    $('.js-reply').button({
            icons: {
                primary: "ui-icon-comment"
            },
            text: false
    });

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
   })










