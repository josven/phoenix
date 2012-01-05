jQuery(document).ready(function() {
    
    $('.js-reply').click( function (event) {
        event.preventDefault();
        
        var entry = $(this).parentsUntil('ul').last(),
            content = entry.find('.entry-content').clone();
        
        entry.addClass('ui-state-active');
        
        dialog = content.dialog({
            width: "500",
            title: "Svara " + $(this).data('replyTo'),
            buttons: {
                    "Svara": function() {
                        dialog.find('form').submit();
                    },
                    Cancel: function() {
                        $( this ).dialog( "close" );
                    }
            },
            close: function(event, ui) { 
                entry.removeClass('ui-state-active');
            },
        });
        
        dialog.find('div.ui-helper-hidden').show();
        dialog.find('textarea').val('');
        dialog.find('p.ui-helper-hidden').hide();
        
    entry.addClass('ui-state-active');
        return false;
    });
    
    // Activate/deavivate reply
    $('.full_width_reply textarea').focus( function () {
        var item = $(this).parentsUntil('.subthread').last();
        $(this).animate({height: '200',});
        item.find('p.ui-helper-hidden').show();
    });
        
    $('.js-collapse').click( function (event) {
        event.preventDefault();
        var item = $(this).parentsUntil('.subthread').last();   
        console.log( item );
        
        item.find('textarea').animate({height: '25',});        
        item.find('p.ui-helper-hidden').hide();
        return false;
    });
    
    
    // Apply datatables
    $('#table_threads').dataTable({
        "aaSorting": [[6,'desc']],
        "bJQueryUI": true,
        "oLanguage": {
            "sLengthMenu": "Visar _MENU_ artiklar per sida",
            "sZeroRecords": "Hittade ingeting =(",
            "sInfo": "Visar _START_ till _END_ av _TOTAL_ artiklar",
            "sInfoEmpty": "Visar 0 till 0 av 0 artiklar",
            "sInfoFiltered": "(filtrerat från _MAX_ antal artiklar)",
            "sSearch": "Filter"
        },
        "iDisplayLength": 50,
        "aoColumns": [ 
			null,
			null,
			null,
			null,
			null,
			null,
			{ "bVisible":    false },
		]
    });
});