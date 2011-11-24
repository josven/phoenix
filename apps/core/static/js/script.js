$(document).ready(function() {

    // Apply jQuery UI buttons
    $( "input:submit, a.ui-button,nav a, button").button();

    // Show messages with jGrowl
    var messages = $('.jGrowlmessages li');
    messages.hide();
    messages.each( function(){
        $.jGrowl(this.innerHTML);
    });
});


















