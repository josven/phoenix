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
   $('.entry-content:containsinsensitive("'+username+':")').parent('li').addClass('ui-state-active');

   
   // Auto update
   
   var auto_refresh = setInterval(
    function ()
    {
       if ( $('#autoupdate').is(':checked') ) {
           $.ajax({
              url: window.location.pathname,
              data: {'s':$("li:[data-id]").first().data('id')},
              success: function(data) {
                if( data["status"] != 302) {
                    var amount = $('#chatlist li.entry').length;
                    $(data).hide().prependTo("#chatlist").fadeIn("slow");
                    $('#chatlist li.entry:gt(49)').fadeOut().remove()
              }}
            });
        }
    }, 10000); // refresh every 10000 milliseconds

    $( "#autoupdate" ).button();
   
   

   
   
});