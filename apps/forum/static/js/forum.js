jQuery(document).ready(function() {
    
    //Fix all the orphan-forms
    $('.orphan-form').each( function () {
        var parent_id = $(this).parents('ul').first().children('li.entry').last().find('#id_parent_id').val();
        console.log( parent_id );
        console.log( $(this).find('#id_parent_id').attr('value') );
        $(this).find('#id_parent_id').attr('value',parent_id); 
        
    });
    
    $('.js-reply').click( function (event) {
        event.preventDefault();
        
        var entry = $(this).parentsUntil('ul').last(),
            content = entry.find('.entry-content').first().clone();
        
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
        
        dialog.find('input.save_method').attr('value','reply');
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
        "bAutoWidth": false,
        "aaSorting": [[5,'desc']],
        "bJQueryUI": true,
        "oLanguage": {
            "sLengthMenu": "Visar _MENU_ trådar per sida",
            "sZeroRecords": "Hittade ingeting =(",
            "sInfo": "Visar _START_ till _END_ av _TOTAL_ trådar",
            "sInfoEmpty": "Visar 0 till 0 av 0 trådar",
            "sInfoFiltered": "(filtrerat från _MAX_ antal trådar)",
            "sSearch": "Filter"
        },
        "iDisplayLength": 50,
        "aoColumns": [ 
			null,
			null,
			null,
			null,
			null,
			{ "bVisible":    false },
		]
    });
});