jQuery(document).ready(function() {
    
    oTable = $('#notification_table').dataTable({
        "bAutoWidth": false,
        "aaSorting": [[7,'desc']],
        "bJQueryUI": true,
        "oLanguage": {
            "sLengthMenu": "Visar _MENU_ notifieringar per sida",
            "sZeroRecords": "Inga notifieringar",
            "sInfo": "Visar _START_ till _END_ av _TOTAL_ notifieringar",
            "sInfoEmpty": "Visar 0 till 0 av 0 trådar",
            "sInfoFiltered": "(filtrerat från _MAX_ antal notifieringar)",
            "sSearch": "Filter"
        },
        "iDisplayLength": 30,
        "aoColumns": [ 
			{"sWidth": "10%"},
			{"sWidth": "30%"},
			{"sWidth": "10%"},
			{"sWidth": "10%"},
			{"sWidth": "15%"},
			{"sWidth": "15%", "iDataSort": 7},
            {"sWidth": "10%"},
			{ "bVisible":    false }
		],
        "sDom": '<"H"l<"form_wrapper">fr>t<"F"ip>'
    }); 
    
    /*
    $('#table_latest_guestbook form').submit( function() {
		var sData = $('input', oTable.fnGetNodes()).serialize();
		alert( "The following data would have been submitted to the server: \n\n"+sData );
		return false;
	} );
    */    
    
    
    $('input.button-mark').button();

    
});