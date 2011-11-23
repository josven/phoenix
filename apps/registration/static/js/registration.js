$(document).ready(function() {
    // Apply jQuery UI buttons
    $( "input:submit, a, button").button();
    
    // Modals for register and login. Can be reused for any modalforms
    $( '*[data-modal-form=true]' ).click( function(event) {
        event.preventDefault();
        
        link = this;
        
        var modal = $( '<div id="modal"><form action="' + link.href + '" method="post"></form></div>' );
        $( 'body' ).append( modal );
        $('#modal form').load( link.href + " form ul.formfields" );
        
        modal.dialog( {
            modal: true,
            minWidth: 350,
            position: ["center",100],
            title: link.title,
            buttons: [
                        {
                            text: "Ok",
                            click: function() { $(this).find('form').submit(); }
                        },
                        {
                            text: "Avbryt",
                            click: function() { $(this).dialog("close"); }
                        }
                     ],
        });
        
        return false;
    });
});
