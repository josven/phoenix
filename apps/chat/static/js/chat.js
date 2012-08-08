var updateChat = function() {

    $.ajax({
        url: window.location.pathname + "get/",
        data: {
            's': $("li:[data-id]").first().data('id')
            },
        statusCode: {
            200: function(data) {
                $('#chatlist .loading-message').fadeOut().remove();
                var amount = $('#chatlist li.entry').length;
                $(data).hide().prependTo("#chatlist").slideDown("slow");
                $('#chatlist li.entry:gt(49)').fadeOut().remove();
                formatJsReplyButton();
                formatImageDialogs();
                bindReplyButton();

                $('#chatt-form-post textarea, #chatt-form-post input').prop('disabled', false);
                $('#chatt-form-post input').removeClass('ui-state-hover');
                processing = false;
            }
        }
    });
};

// Reply link event
var bindReplyButton = function() {

    $('a.js-reply').unbind('click').click(function(e) {
        e.preventDefault();

        var to = $(this).data('replyTo'),
        textarea = $('form#chatt-form-post textarea'),
        text = textarea.val();

        // if there any whitespace at the end.
        if (/\s$/g.test(text)) {
            textarea.val(text + to + ": ").putCursorAtEnd();
        } else {
            textarea.val(text + " " + to + ": ").putCursorAtEnd();
        }
        return false;
    });
};

jQuery(document).ready(function() {
    
    // tinychat
    $('.tinychat_embed').css({
        'height': '85%',
        'margin-top': '3%'
    });

    updateChat();
    bindReplyButton();
    formatJsMaximizeButton();

    // Hi(A)ja(x)ck form
    $('#chatt-form-post').submit(function(event) {
        event.preventDefault();

        var form = $(this),
        formData = form.serialize();

        $.ajax({
            type: "POST",
            url: form.attr('action'),
            cache: false,
            data: formData,
            beforeSend: function() {
                $('#chatt-form-post textarea, #chatt-form-post input').prop('disabled', true);
                clearInterval(auto_refresh);
            },
            statusCode: {
                200: function(data) {
                    $('#chatt-form-post textarea').val('');
                    updateChat();
                    auto_refresh = setInterval(function() {
                        if ($('#autoupdate').is(':checked')) {
                            updateChat();
                        }
                    }, 10000);
                    // refresh every 10000 milliseconds
                    }
            },
            error: function(data) {
                console.log(data);
                $('#chatt-form-post textarea, #chatt-form-post input').prop('disabled', false);
            }
        });
        return false;

    });

    // Auto update
    var auto_refresh = setInterval(function() {
        if ($('#autoupdate').is(':checked')) {
            updateChat();
        }
    }, 10000);
    // refresh every 10000 milliseconds
    $("#autoupdate").button();
});