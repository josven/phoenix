jQuery(document).ready(function() {
    
    
    var table_threads = $('#table_threads').dataTable({
        "bServerSide": true,
        "bJQueryUI": true,
        "aaSorting": [[3,'desc']],
        "bAutoWidth": false,
        "oLanguage": {
            "sLengthMenu": "Visar _MENU_ trådar per sida",
            "sZeroRecords": "Hittade ingeting =(",
            "sInfo": "Visar _START_ till _END_ av _TOTAL_ trådar",
            "sInfoEmpty": "Visar 0 till 0 av 0 trådar",
            "sInfoFiltered": "(filtrerat från _MAX_ antal trådar)",
            "sSearch": "Sök bland trådtitlar"
        },
        "sAjaxSource": window.location.pathname + "json/",
        "aoColumns": [
                        { "mDataProp": "title", "bSortable": false},
                        { "mDataProp": "tags" , "bSortable": false, "bSearchable" : false},
                        { "mDataProp": "created", "iDataSort": 3 , "bSearchable" : false},
                        { "mDataProp": "index", "bVisible": false, "bSearchable" : false},
                        { "mDataProp": "posts_index" , "bSortable": false, "bSearchable" : false},
                        { "mDataProp": "last_comment", "iDataSort": 6 , "bSearchable" : false},
                        { "mDataProp": "last_comment_index", "bVisible": false , "bSearchable" : false},
                        
                ],
        "fnDrawCallback": function() {
            $('.ui-tag a').button( { icons: {primary:'ui-icon-tag'}} );
        }
    });    


    $( "#tabs" ).tabs();

    // Soring tabs
    $('.js-sort-latest-threads').click( function () {
        table_threads.fnSort( [ [3,'desc'] ] );

    });
    
    $('.js-sort-latest-replies').click( function () {
        table_threads.fnSort( [ [5,'desc'] ] );
    });

    $('.forumtree .accordion').accordion({
        collapsible: true,
        active: false,            
    });
    
        
    $('.forumtree .js-reply').click( function (event) {
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
        
        dialog.find('form.ui-helper-hidden').show();
        dialog.find('textarea').val('');
        dialog.find('p.ui-helper-hidden').hide();
        
    entry.addClass('ui-state-active');
        return false;
    });
    
    
    
    
    
    
    
    
    
    
    
    /* OLD STUFF */
    // Really ugly hack, until the forum are fully fixed =(
    // This removes replys that gets outside the main thread
    $('.thead_wrapper .subthread').first().siblings().remove();
    
    //Fix all the orphan-forms
    $('.orphan-form').each( function () {
        var parent_id = $(this).parents('ul').first().children('li.entry').last().find('#id_parent_id').val();
        console.log( parent_id );
        console.log( $(this).find('#id_parent_id').attr('value') );
        $(this).find('#id_parent_id').attr('value',parent_id); 
        
    });
    
    $('.oldforum .js-reply').click( function (event) {
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

    $('#notification_table').dataTable({
        "bAutoWidth": false,
        "aaSorting": [[5,'desc']],
        "bJQueryUI": true,
        "oLanguage": {
            "sLengthMenu": "Visar _MENU_ notifieringar per sida",
            "sZeroRecords": "Inga notifieringar",
            "sInfo": "Visar _START_ till _END_ av _TOTAL_ notifieringar",
            "sInfoEmpty": "Visar 0 till 0 av 0 notifieringar",
            "sInfoFiltered": "(filtrerat från _MAX_ antal notifieringar)",
            "sSearch": "Filter"
        },
        "iDisplayLength": 30,
        "aoColumns": [ 
			{"sWidth": "50%"},
			{"sWidth": "10%"},
			{"sWidth": "15%"},
			{"sWidth": "20%"},
			{"sWidth": "5%", "iDataSort": 5},
			{ "bVisible":    false }
		],
        "sDom": '<"H"l<"form_wrapper">fr>t<"F"ip>'
    });    
    
    $('input.button-mark').button();    

});