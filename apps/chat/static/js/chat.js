jQuery(document).ready(function() {    
    // Reply link event
    $('a.js-reply').click( function (e) {
        e.preventDefault();
        
        var to = $(this).data('replyTo'),
            textarea = $('form#chat_form textarea'),
            text = textarea.val();
        
        // if there any whitespace at the end.
        if ( /\s$/g.test(text) ) {
            textarea.val( text + to + ": ").putCursorAtEnd();
        } else {
            textarea.val( text + " " + to + ": ").putCursorAtEnd();
        }
        return false;
    });
   
   // Hilight a messages with usename.
   var username = $('#username').html();
   $('.entry-content:containsinsensitive("'+username+'")').parent('li').addClass('ui-state-active');

   
});