// Formatera jQuery UI för denna app
var formatjQueryUI = function() {

    formatJsReplyButton();
    formatJsHistoryButton();
    formatJsDeleteButton();
    formatJsEditButton();
    formatJsMaximizeButton();

    // Buttons
    $('input:submit, a.ui-button, button').button();

    // Buttonsets
    $('.buttonset').buttonset();

    // Svara knappen
    $('.js-reply').click( function(event) {
        event.preventDefault();

        var button = $(this),
            form_id = button.data('form'),
            formwrapper = $('#'+form_id).parent(),
            comment_id = button.data('comment'),
            comment = $('#'+comment_id),
            parent_id = button.data('commentId'),
            article_id = formwrapper.data('articleId');     

        // reset
        resetEntries();
        formwrapper.find('.toggle-rel-threads').css( 'visibility', 'hidden' );

        // Visar svarsknappen för huvudartiklen
        $('#btn-comment-'+ String(article_id) ).css('visibility','visible');

        comment.addClass('ui-state-highlight');
        formwrapper.find('input[name=parent_id]').val( parent_id );
        formwrapper.insertAfter(comment).hide().slideDown( function(){
            $('html, body').animate({
                 scrollTop: formwrapper.offset().top - $(window).height() + formwrapper.outerHeight()
             }, 500);
        });

        return false;
    });

    // Fortsätt knappen (svara alla)
    $('.js-reply-all').click( function(event){
        event.preventDefault();

        // Variabler
        var button = $(this),
            form = $('#'+button.data('form')).parent(),
            hasChildrens = !(typeof button.data('hasChildren') === "undefined"),
            article_id = form.data('articleId');
                
        if (hasChildrens) {
            // Om commentaren redan har svar, så svaret komma längst ned
            var root_comment_selector = "#" + String( button.data('comment') );
        } else {
            // Om inte kommentaren har svar, så är det en kommentar mitt i en tråd
            var root_comment_selector = "#" + String( button.parents('ul').first().prev().attr('id') );
        }

        var root = $( root_comment_selector ),
            entrys = $(root_comment_selector + ' + ul > li > div.comment-entry').add( root ),
            subthreads = $(root_comment_selector + ' + ul > li > ul.list-comments');

        // reset
        resetEntries();
        form.find('.toggle-rel-threads').css( 'visibility', 'hidden' );

        // Visar svarsknappen för huvudartiklen
        $('#btn-comment-'+ String(article_id) ).css('visibility','visible');

        // Aktiverar relevata inlägg
        entrys.addClass('ui-state-highlight');

        // Gömmer subtrådar
        subthreads.addClass('ui-helper-hidden');

        // Stoppar in formuläret på rätt plats
        form.find('input[name=parent_id]').val( root.data('commentId') );
        form.insertAfter( entrys.last() );
        
        // Visar knapp för att toggla relevanta inlägg
        if (subthreads.length > 0) {

            // Skickar ett medelande via jGrowl
            $.jGrowl( "Gömmer " + String(subthreads.length) + " orelevanta subtrådar.");

            // Toggle logik
            form.find('.toggle-rel-threads').css( 'visibility','visible' );
            form.find('input[type=checkbox].toggle-rel-threads').attr("checked", "checked").button("refresh").click( function (event) {
                if ( this.checked ) {
                    subthreads.addClass('ui-helper-hidden');
                } else {
                    subthreads.removeClass('ui-helper-hidden');
                };

                $('html, body').animate({
                    scrollTop: form.offset().top - $(window).height() + form.outerHeight()
                }, 500);
            });
        };

        // Scrollar till formuläret
        $('html, body').animate({
            scrollTop: form.offset().top - $(window).height() + form.outerHeight()
        }, 500);
        

        return false;
    });
};




jQuery(document).ready(function() {

    formatjQueryUI();

    // Kommentarknappen för artiklen som visar formuläret
    $('.btn-comment-article').click( function (event) {
        event.preventDefault();

        var button = $(this),
            form = $('#' + button.data('form')).parent(),
            container = $('#' + button.data('container'));

        // Reset
        resetEntries();
        form.find('.toggle-rel-threads').css( 'visibility', 'hidden' );
        
        form.find('input[name=parent_id]').val( "" );
        form.prependTo(container);
        button.css('visibility','hidden');

        return false;
    });


    //Ajaxifiera formulären
    $("body").on("submit", "form.form-add-entry", function(event) {
        event.preventDefault();

        var form = $(this),
            url = form.attr('action'),
            data = form.serialize(),
            button = form.find('input[type=submit]'),
            loader = $('&nbsp;<img src="/static/img/ajax-loader.gif" class="gif-submit-loader" alt="Wakawakawakawakawaka..." />'),
            cont = $('#'+form.data('container') );

        form.find('input, textarea').attr('disabled', 'disabled');
        button.parent().append( loader );

        $.ajax({
            type: "POST",
            url: url,
            data: data,
            dataType: "html",
            success: function(data, textStatus, jqXHR) {
                if ( jqXHR.status === 278 ) {
                    window.location.href = jqXHR.getResponseHeader("Location");
                }
                else {
                    cont.html(data);
                    formatjQueryUI();
                    $.jGrowl('close');
                }
            }
        });

        return false;
    });

    // Visa kommentarer
    $('.js-show-comments').click(function(event) {
        event.preventDefault();
        
        var button = $(this),
            loader = $('&nbsp;<img src="/static/img/ajax-loader.gif" class="gif-submit-loader" alt="Wakawakawakawakawaka..." />');

        button.parent().after( loader );
        button.addClass('ui-state-highlight');

        var btn = $(this),
            url = btn.data('url'),
            cont = $('#'+btn.data('container') );
         
        cont.load(url, function(){
            loader.remove();
            button.removeClass('ui-state-highlight');
            formatjQueryUI();
        });

        return false;
    });

    var table_threads = $('#table_threads').dataTable({
        "bServerSide": true,
        "bJQueryUI": true,
        "iDisplayLength": 30,
        "aaSorting": [[3, 'desc']],
        "bAutoWidth": false,
        "oLanguage": {
            "sLengthMenu": "Visar _MENU_ trådar per sida",
            "sZeroRecords": "Hittade ingeting =(",
            "sInfo": "Visar _START_ till _END_ av _TOTAL_ trådar",
            "sInfoEmpty": "Visar 0 till 0 av 0 trådar",
            "sInfoFiltered": "(filtrerat från _MAX_ antal trådar)",
            "sSearch": "Sök bland trådartitlar"
        },
        "sAjaxSource": window.location.pathname + "json/",
        "aoColumns": [{
            "mDataProp": "title",
            "bSortable": false
        }, {
            "mDataProp": "tags",
            "bSortable": false,
            "bSearchable": false
        }, {
            "mDataProp": "created",
            "iDataSort": 3,
            "bSearchable": false
        }, {
            "mDataProp": "index",
            "bVisible": false,
            "bSearchable": false
        }, {
            "mDataProp": "posts_index",
            "bSortable": false,
            "bSearchable": false
        }, {
            "mDataProp": "last_comment",
            "iDataSort": 6,
            "bSearchable": false
        }, {
            "mDataProp": "last_comment_index",
            "bVisible": false,
            "bSearchable": false
        }],
        "fnPreDrawCallback": function( oSettings ) {
            $("body").css("cursor", "progress");
        },
        "fnDrawCallback": function() {
            $("body").css("cursor", "auto");
            render_tags();
        }
    });

    $("#tabs").tabs();

    // Sorting tabs
    $('.js-sort-latest-threads').click(function() {
        table_threads.fnSort([[3, 'desc']]);

    });

    $('.js-sort-latest-replies').click(function() {
        table_threads.fnSort([[5, 'desc']]);
    });

});