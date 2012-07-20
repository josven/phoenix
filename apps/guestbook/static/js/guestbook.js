/*
* Format guestbook replybutton
*
*/
var formatJsReplyGuestbookButton = function () {
    $('.js-reply').click(function(event) {
        event.preventDefault();

        var button = $(this),
            entry_selector = "#" + button.data('comment'),
            entry = $(entry_selector),
            form_selector = "#" + button.data('form'),
            form = $(form_selector),
            user_id = button.data('userId');

            // Visar formuläret samt flyttar den under inlägget.
            form.removeClass('ui-helper-hidden').insertAfter(entry);

            // Sätter ID för vems gästbok man ska svara i.
            $( form_selector + " #id_user_id").val( user_id );

            // Sätter ny url för formuläret
            form.attr('action',this.href);

        return false;
    });
};


/*
* Konveration History entry button
*
*/
var formatJsConversationButton = function () {
    $('.js-entry-conversation').button({
        icons: {
            primary: "ui-icon-transferthick-e-w"
        }
    });
};

/*
* Delete guestbook button
*
*/
var formatJsDeleteGuestbookButton = function () {
    $('.js-delete-guestbook-entry').click(function(event) {
        event.preventDefault();

        var button = $(this),
            entry_selector = "#" + button.data('comment'),
            url = this.href,
            entry = $(entry_selector);

            var dialog = $('<div></div>').load(url, function(){
                $(this).dialog({
                        modal: true,
                        title: "Radera?",
                        buttons: {
                            "Radera": function() {
                                $.ajax({
                                    type: "POST",
                                    url: url,
                                    data: dialog.find('form').serialize(),
                                    statusCode: {
                                        200: function(data) {
                                            dialog.dialog("close");
                                            entry.fadeOut().remove();
                                            $.jGrowl('Meddelandet borttaget!');
                                        },
                                        428: function(data) {
                                            dialog.append('<p style="font-style:bold;">Du måste välja om du ska fortsätta</p>');
                                        }
                                    }
                                });
                            },
                            "Avbryt": function() {
                                dialog.dialog("close");
                            }
                        }
                    });
                });

        return false;
    });
};

jQuery(document).ready(function() {

    formatJsMaximizeButton();
    formatJsConversationButton();
    formatJsDeleteGuestbookButton();
    formatJsReplyGuestbookButton();



    //Ajaxifiera formulären
    $("body").on("submit", "form.form-add-entry", function(event) {
        event.preventDefault();

        var form = $(this),
            url = form.attr('action'),
            formdata = form.serialize(),
            button = form.find('input[type=submit]'),
            loader = $('&nbsp;<img src="/static/img/ajax-loader.gif" class="gif-submit-loader" alt="Wakawakawakawakawaka..." />'),
            form_inputs = form.find('input, textarea'),
            form_wrapper = $('#guestbook-form-wrapper');

        form_inputs.attr('disabled', 'disabled');
        button.parent().append( loader );
        

        $.ajax({
            type: "POST",
            url: url,
            data: formdata,
            success: function(data, textStatus, jqXHR) {
                $.jGrowl('Meddelande skickat!');
                loader.remove();

                // Återställer formuläret
                form_inputs.removeAttr('disabled');
                form.find('textarea').val('');
                form.appendTo( form_wrapper );

                $('#guestbook-entries').html(data);
                formatJsConversationButton();
                formatJsDeleteGuestbookButton();
                formatJsReplyGuestbookButton();
                formatPagnation();
                $('.buttonset').buttonset();

            }
        });

        return false;
    });
    $('#switcher').themeswitcher();
});