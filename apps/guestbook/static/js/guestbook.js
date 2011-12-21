jQuery(document).ready(function() {

    $('.js-reply').click( function () {
        var entry = $(this).parentsUntil('ul').last(),
            content = entry.find('.ui-text-panel').clone();
        
        dialog = content.dialog({
            title: "Svara " + $(this).data('replyTo'),
            buttons: {
                    "Svara": function() {
                        dialog.find('form').submit();
                    },
                    Cancel: function() {
                        $( this ).dialog( "close" );
                    }
            }
        });
        
        dialog.find('.ui-helper-hidden').show();
        dialog.find('.entry-profile-picture').hide();

    });

});