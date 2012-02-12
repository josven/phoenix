jQuery(document).ready(function() {

    
    $('.js-reply').click( function (event) {
        event.preventDefault();
        
        var entry = $(this).parentsUntil('ul').last(),
            content = entry.find('.entry-content').clone();
        
        var dialog = content.dialog({
            width: 600,
            title: "Svara " + $(this).data('replyTo'),
            buttons: {
                    "Svara": function() {
                        form = dialog.find('form');

                        $.ajax( {
                            type: "POST",
                            url: form.attr( 'action' ),
                            data: form.serialize(),
                            statusCode: {
                                200: function() {
                                    entry.removeClass('ui-state-active');
                                    entry.find('.delete-notification-form').remove();
                                    dialog.dialog( "close" );
                                }
                            }  
                        });

                    },
                    "Förhandsgranska": function() {
                        var form = dialog.find('form');
                        var preview = "text";
                        preview_textarea(form, preview);
                    },
                    Cancel: function() {
                        dialog.dialog( "close" );
                    }
            }
        });
        
        dialog.find('.ui-helper-hidden').show();
        
        dialog.find('textarea').autoResize({
            // Quite slow animation:
            animateDuration : 300,
        });

        return false;
    });

});