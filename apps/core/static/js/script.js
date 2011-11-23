$(document).ready(function() {
    
    // Show messages with jGrowl
    var messages = $('.jGrowlmessages li');
    messages.hide();
    messages.each( function(){
        $.jGrowl(this.innerHTML);
    });
});


















