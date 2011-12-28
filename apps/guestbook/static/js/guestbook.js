jQuery(document).ready(function() {

    $('.js-reply').click( function (event) {
        event.preventDefault();
        
        var entry = $(this).parentsUntil('ul').last(),
            content = entry.find('.entry-content').clone();
        
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
        
        return false;
    });

});