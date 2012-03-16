jQuery(document).ready(function() {

    $('#id_allow_comments').button();

    $('.js-reply').click(function(event) {
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
                "FР вЂ›Р’В¶rhandsgranska": function() {
                    var form = dialog.find('form');
                    var preview = "comment";
                    preview_textarea(form, preview);
                },
                Cancel: function() {
                    $(this).dialog("close");
                }
            },
            close: function(event, ui) {
                entry.removeClass('ui-state-active');
            }
        });

        dialog.find('form.ui-helper-hidden').show();
        dialog.find('textarea').val('');
        dialog.find('p.ui-helper-hidden').hide();

        entry.addClass('ui-state-active');

        dialog.find('textarea').autoResize({
            // On resize:
            onResize: function() {
                $(this).css({
                    opacity: 0.8
                });
            },
            // After resize:
            animateCallback: function() {
                $(this).css({
                    opacity: 1
                });
            },
            // Quite slow animation:
            animateDuration: 300,
            // More extra space:
            extraSpace: 40
        });

        return false;
    });

    // quick edit button
    $('.js-quick-edit').button({
        icons: {
            primary: "ui-icon-pencil"
        }
    }).click(function(event) {
        event.preventDefault();

        var button = $(this),
        url = button.attr('href'),
        field = $("#" + button.attr('rel')),
        initalHeight = field.height();

        // load form
        field.load(url, function() {
            field.find('label').remove();
            field.find('textarea').css({
                'height': initalHeight,
                'min-height': 300
            });
        });

        // change to save button
        button.replaceWith('  <a href="http://sv.wikipedia.org/wiki/Textile" class="js-help" target="_blank">Hjälp</a><a href="' + url + '" class="js-quick-save" rel="article-body">Spara</a>');
        $('.js-quick-save').button({
            icons: {
                primary: "ui-icon-pencil"
            }
        }).click(function(event) {
            event.preventDefault();
            field.find('form').submit();
        });

        $('.js-help').button({
            icons: {
                primary: "ui-icon-help"
            }
        }).parent().buttonset();
        return false;
    });

    // Select categories
    $(".categories").selectable({
        stop: function() {
            var tags = "";
            $(".ui-selected", this).each(function() {
                var tag = this.innerHTML;
                tags = tags + " " + tag;

            });
            $("#id_tags").val(tags.trim());
        }
    }).on('mousedown', '*', function(e) {
        // fix http://bugs.jqueryui.com/ticket/7858
        if (e.ctrlKey) {
            e.metaKey = e.ctrlKey;
        }
    });

    $('#table_articles').dataTable({
        "bServerSide": true,
        "bJQueryUI": true,
        "aaSorting": [[4, 'desc']],
        "bAutoWidth": false,
        "oLanguage": {
            "sLengthMenu": "Visar _MENU_ artiklar per sida",
            "sZeroRecords": "Hittade ingeting =(",
            "sInfo": "Visar _START_ till _END_ av _TOTAL_ artiklar",
            "sInfoEmpty": "Visar 0 till 0 av 0 artiklar",
            "sInfoFiltered": "(filtrerat från _MAX_ antal artiklar)",
            "sSearch": "Sök bland artikeltitlar"
        },
        "sAjaxSource": window.location.pathname + "json/",
        "aoColumns": [{
            "mDataProp": "title",
            "bSortable": false
        }, {
            "mDataProp": "created",
            "iDataSort": 4,
            "bSearchable": false
        }, {
            "mDataProp": "tags",
            "bSortable": false,
            "bSearchable": false
        }, {
            "mDataProp": "allow_comments",
            "bSearchable": false,
            "bSortable": false
        }, {
            "mDataProp": "id",
            "bSortable": true,
            "bSearchable": false,
            "bVisible": false
        }],
        "fnDrawCallback": function() {
            $('.ui-tag a').button({
                icons: {
                    primary: 'ui-icon-tag'
                }
            });
        }
    });

    $('#notification_table').dataTable({
        "bAutoWidth": false,
        "aaSorting": [[5, 'desc']],
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
        "aoColumns": [{
            "sWidth": "50%"
        }, {
            "sWidth": "10%"
        }, {
            "sWidth": "15%"
        }, {
            "sWidth": "20%"
        }, {
            "sWidth": "5%",
            "iDataSort": 5
        }, {
            "bVisible": false
        }],
        "sDom": '<"H"l<"form_wrapper">fr>t<"F"ip>'
    });

    $("#tabs").tabs();

});