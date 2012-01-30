
var updateChat = function() {
   $.ajax({
      url: window.location.pathname,
      data: {'s':$("li:[data-id]").first().data('id')},
      success: function(data) {
        if( data["status"] != 302) {
            var amount = $('#chatlist li.entry').length;
            $(data).hide().prependTo("#chatlist").fadeIn("slow");
            $('#chatlist li.entry:gt(49)').fadeOut().remove();
            formatJsReplyButton();
            formatImageDialogs();
            bindReplyButton();
            hilightUserName();
            $('#chat_form textarea, #chat_form input').prop('disabled', false);
            $('#chat_form input').removeClass('ui-state-hover');
      }}
    });
}

// Reply link event
var bindReplyButton = function () {
    
    $('a.js-reply')
        .unbind('click')
        .click(function (e) {
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
}

// Hilight a messages with usename.
var hilightUserName = function() {
   var username = $('#username').html();
   $('.entry-content:containsinsensitive("'+username+':")').parent('li').addClass('ui-state-active');
}


jQuery(document).ready(function() {    
    

   // tinychat
    $('.tinychat_embed').css({'height':'85%','margin-top':'3%'});

    bindReplyButton();
    hilightUserName();
    
   // Hi(A)ja(x)ck form
   $('#chat_form').submit( function(event) {
        if( $('#autoupdate').is(':checked') ) {
            event.preventDefault();
            var formData = $("#chat_form").serialize();
            $.ajax({
                type: "POST",
                url: window.location.pathname,
                cache: false,
                data: formData,
                beforeSend: function( ) {
                    $('#chat_form textarea, #chat_form input').prop('disabled', true);
                },
                success: function () {
                    $('#chat_form textarea').val('');
                    $.jGrowl('Medelande skickat!');
                    updateChat();
                },
                error: function () {
                    $.jGrowl('Något blev fel!');
                    $('#chat_form textarea, #chat_form input').prop('disabled', false);
                }
            });
            return false;
        }
   });
        
   // Auto update
   var auto_refresh = setInterval(
    function ()
    {
       if ( $('#autoupdate').is(':checked') ) {
            updateChat();
        }
    }, 10000); // refresh every 10000 milliseconds

    $( "#autoupdate" ).button();

});