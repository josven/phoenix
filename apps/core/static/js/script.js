$(document).ready(function() {

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










