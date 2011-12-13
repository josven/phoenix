$(document).ready(function() {

    // Apply jQuery UI buttons
    $( "input:submit, a.ui-button,nav a, button").button();
    $( ".buttonset" ).buttonset();

    // Show messages with jGrowl
    var messages = $('.jGrowlmessages li, .errorlist li');
    messages.hide();
    messages.each( function(){
        $.jGrowl(this.innerHTML);
    });
    
    // User jQuery datepicker
    $(".datepicker").datepicker({dateFormat: 'yy-mm-dd', defaultDate:'-25y',  changeYear: true, changeMonth: true });
});


















