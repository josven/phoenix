jQuery(document).ready(function() {
    
    // Select categories
    $( "#categories" ).selectable({
			stop: function() {
				var tags = "";				
                $( ".ui-selected", this ).each(function() {
					var tag = this.innerHTML;
					tags = tags + " " + tag;
                    
				});
                $( "#id_tags" ).val(tags.trim());
			}
        }).on('mousedown', '*', function(e){
            // fix http://bugs.jqueryui.com/ticket/7858
            if (e.ctrlKey) {
                e.metaKey = e.ctrlKey;
            }
        });
    
    // Reply button
    jQuery(".js-reply").click(function() {
        var button = $(this),
            item = $(this).parents('.forum_post').next();
       
        item.fadeToggle('fast', function() {
            // Animation complete.
            item.find('textarea').putCursorAtEnd();
            item.is(':visible') ? button.addClass('ui-state-highlight') : button.removeClass('ui-state-highlight');
          }).removeClass('ui-helper-hidden');
        
        
        //$( this ).toggleClass('ui-state-highlight');
        
        return false;
    });
    
    // Activate/deavivate reply
    $('.inactive_reply textarea').focus( function () {
        var item = $(this).parentsUntil('.subthread').last();
        
        item.removeClass('inactive_reply');
        item.addClass('ui-state-active');
        item.find('p.ui-helper-hidden').show();
        item.prev().find('.js-reply').addClass('ui-state-highlight');
    });
    
    
    // Apply datatables
    $('#table_threads').dataTable({
        "bJQueryUI": true,
        "oLanguage": {
            "sLengthMenu": "Visar _MENU_ artiklar per sida",
            "sZeroRecords": "Hittade ingeting =(",
            "sInfo": "Visar _START_ till _END_ av _TOTAL_ artiklar",
            "sInfoEmpty": "Visar 0 till 0 av 0 artiklar",
            "sInfoFiltered": "(filtrerat från _MAX_ antal artiklar)",
            "sSearch": "Filter"
        }
    });
});