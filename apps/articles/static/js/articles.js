jQuery(document).ready(function() {

$('#id_allow_comments').button();

$('.accordion').accordion({
			collapsible: true,
            active: false,            
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
        
        dialog.find('form.ui-helper-hidden').show();
        dialog.find('textarea').val('');
        dialog.find('p.ui-helper-hidden').hide();
        
    entry.addClass('ui-state-active');
        return false;
    });
    
    // quick edit button
    $('.js-quick-edit').button({
                            icons: {
                                primary: "ui-icon-pencil"
                            }
                        })
                        .click( function ( event ) {
                            event.preventDefault();
                            
                            var button = $( this ),
                                url = button.attr( 'href' ),
                                field = $( "#"+button.attr( 'rel' ) ),
                                initalHeight = field.height();
                                
                            // load form
                            field.load(  url , function () {
                                field.find('label').remove();
                                field.find('textarea').css( {'height': initalHeight,'min-height':300} );
                            });

                            // change to save button
                            button.replaceWith( '  <a href="http://sv.wikipedia.org/wiki/Textile" class="js-help" target="_blank">Formateringshjälp</a><a href="'+ url +'" class="js-quick-save" rel="article-body">Spara</a>');
                            $( '.js-quick-save' ).button({
                                icons: {
                                    primary: "ui-icon-pencil"
                                }
                            }).
                            click( function ( event ) {
                                event.preventDefault();
                                field.find('form').submit();
                            });
                            
                            $( '.js-help' ).button({
                                                  icons: {
                                                        primary: "ui-icon-help"
                                                    }
                            }).parent()
                                .buttonset();                            
                            return false;
                        });
  
    // Select categories
    $( ".categories" ).selectable({
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
    
    // Apply datatables
    $('#table_articles').dataTable({
        "bAutoWidth": false,
        "aaSorting": [[4,'desc']],
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
			{ "bVisible":    false },
		]
    });
});