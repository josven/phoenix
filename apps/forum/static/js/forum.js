jQuery(document).ready(function() {
    
    /*
	jQuery(".full_width_reply textarea").autoResize({
        minHeight: 50
    });
    */
    
    jQuery(".ui-button-reply").click(function() {
        $(this).parents('.forum_post').next().fadeToggle('fast', function() {
            // Animation complete.
          }).removeClass('ui-helper-hidden');
          
        $( this ).toggleClass('ui-state-highlight');
        
        return false;
    });
});