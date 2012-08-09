// Some vars
var testvar;
var update_data = {"n":true};


/*
* process_updates
*
*/

var process_updates = function (data) {

    // Notifikationräknare
    if ( data.hasOwnProperty('notification_count') ) {
        $('#notification-counter').html("("+ data.notification_count +")");
        window.parent.document.title = "("+ data.notification_count +") PHX";
    }

    // Notifikation annonserare
    if ( data.hasOwnProperty('notification_message') ) {
        $.jGrowl(data.notification_message);
    }
};

/*
* auto_update
*
*/
var auto_update = function() {
    setInterval(function() {

        var pass = false;

        if (Modernizr.localstorage) {

            if ( window.localStorage.hasOwnProperty("update_data_timestamp") ) {

                var now = Number( new Date().getTime()),
                    then = Number( window.localStorage.getItem("update_data_timestamp") ),
                    delta = ( now - then );
                    if ( delta > 30000) {
                        pass = true;
                    } else {
                        var stored_data = window.localStorage.getItem("update_data"),
                            stored_json_data = JSON.parse(stored_data);

                        process_updates(stored_json_data);
                    }
            } else {
                pass = true;
            }
        } else {
            pass = true;
        }

        if (pass === true) {
            $.ajax({
                data: update_data,
                contentType: "application/json; charset=UTF-8",
                dataType: "json",
                url: "/notifications/updates.json",
                success: function(data) {                        
                    if (Modernizr.localstorage) {
                        var timestamp = new Date().getTime();
                        window.localStorage.setItem("update_data_timestamp", timestamp);
                        window.localStorage.setItem("update_data", JSON.stringify(data));
                    }
                    
                    process_updates(data);
                },
                error: function(data) {
                    console.log("Något fel har inträffat");
                }
            });
        }

    }, 30000); // refresh every 30000 milliseconds
};


/*
* Get search string from GET
*
*/

var highlightEntry = function () {

    var searchObject = searchToObject();

    if ( searchObject.hasOwnProperty('h') ) { 
        var hEntry = $('#'+searchObject.h);

        hEntry.addClass('ui-state-highlight');

        $('html, body').animate({
            scrollTop: hEntry.offset().top - $(window).height() + hEntry.outerHeight()
        }, 500);

    }
};

/*
* Get search string from GET
*
*/
var searchToObject = function () {
  var pairs = window.location.search.substring(1).split("&"),
    obj = {},
    pair,
    i;

  for ( i in pairs ) {
    if ( pairs[i] === "" ) {
        continue;
    }

    pair = pairs[i].split("=");
    obj[ decodeURIComponent( pair[0] ) ] = decodeURIComponent( pair[1] );
  }

  return obj;
};


/*
* Apply jQuery UI on pagination
*
*/

var formatPagnation = function () {
    "use strict";


    $('.pagination').buttonset();
    $('.pagination .disabled').button({
        disabled: true
    });

    $('.pagination .current').button().addClass('ui-state-highlight');
    $('.pagination .elips').button();
};

/*
* Show hidden subthreads
*
*/
var showHiddenSubThreads = function () {
    "use strict";

    var hidden = $('ul.ui-helper-hidden.list-comments');
    hidden.each( function(){
        $(this).find('.comment-entry.ui-state-highlight').removeClass('ui-state-highlight');
    });
    hidden.removeClass('ui-helper-hidden');
};


/*
* deactivate Entries
*
*/
var deactivateEntries = function () {
    "use strict";

    $('div.comment-entry.ui-state-highlight').removeClass('ui-state-highlight');
};


/*
* reset Entries
*
*/
var resetEntries = function () {
    "use strict";

    showHiddenSubThreads();
    deactivateEntries();
};



/*
* Preview button for textareas
*
*/
var formatJsPreviewButton = function () {
    "use strict";

    $('input:[data-preview]').unbind('click').click(function() {
        var form = $(this).parentsUntil('form').parent(),
            preview = $(this).data('preview');
        preview_textarea(form, preview);
    }).parent().buttonset();
};


/*
* Maximize button for forms with textareas
*
*/
var formatJsMaximizeButton = function () {
    "use strict";

    

    $('input:[data-maximize]').unbind('click').click(function() {
        var form_id = $(this).data('form'),
            field_id = $(this).data('field');
        maximize_form(form_id, field_id);

    }).parent().buttonset();
};


/*
* Save entry button
*
*/
var formatJsSaveButton = function () {
    "use strict";
    $('.js-entry-save').button({
        icons: {
            primary: "ui-icon-pencil"
        }
    }).click(function(event) {

        event.preventDefault();
        
        var button = $(this),
            url = button.attr('href'),
            rel = button.attr('rel'),
            field = $("#" + rel);

        $.ajax({
            type: "POST",
            url: url,
            data: field.find('form').serialize(),
            statusCode: {
                200: function(data) {

                    console.log(field);
                    console.log(data);

                    field.html(data);
                        // change to edit button
                        button.replaceWith('<a href="' + url + '" class="js-entry-edit" rel="' + rel + '">&nbsp;</a>');
                        formatJsEditButton();
                }
            }
        });
    }).parent().buttonset();
};

/*
* Edit entry button
*
*/
var formatJsEditButton = function () {
    "use strict";

    $('.js-entry-edit').button({
        icons: {
            primary: "ui-icon-pencil"
        }
    }).click(function(event) {
        event.preventDefault();

        var button = $(this),
            url = button.attr('href'),
            rel = button.attr('rel'),
            field = $("#" + rel);

        // load form
        field.load(url, function() {
            formatJsMaximizeButton();
            formatJsPreviewButton();
        });

        // change to save button
        button.replaceWith('<a href="' + url + '" class="js-entry-save" rel="' + rel + '">&nbsp;Spara</a>');
        formatJsSaveButton();

        return false;
    });
};

/*
* Delete entry button
*
*/
var formatJsDeleteButton = function () {
    "use strict";

    $('.js-entry-delete').button({
        icons: {
            primary: "ui-icon-trash"
        }
    }).click(function(event) {
        event.preventDefault();

        var button = $(this),
            url = button.attr('href'),
            entry = $('#'+button.data('comment'));

        // load form
        var dialog = $('<div></div').load(url).dialog({
            modal: true,
            title: "Radera?",
            buttons: {
                "Radera": function() {
                    $.ajax({
                        type: "POST",
                        url: url,
                        data: dialog.find('form').serialize(),
                        statusCode: {
                            200: function(data) {
                                entry.fadeOut().remove();
                                dialog.dialog("close");
                            },
                            428: function(data) {
                                dialog.append('<p style="font-style:bold;">Du måste välja om du ska fortsätta</p>');
                            }
                        }
                    });
                },
                "Avbryt": function() {
                    dialog.dialog("close");
                }
            }
        });

        return false;
    });
};

/*
* History entry button
*
*/
var formatJsHistoryButton = function () {
    "use strict";

    $('.js-entry-history').button({
        icons: {
            primary: "ui-icon-folder-open"
        }
        }).click(function(event) {
        event.preventDefault();

        var button = $(this),
        url = button.attr('href');

        // load form
        var dialog = $('<div></div').load(url).dialog({
            modal: true,
            title: "Historik",
            width: $(window).width() - 50,
            height: $(window).height() - 150,
            buttons: {
                "Stäng": function() {
                    $(this).dialog("close");
                }
            }
        });

        return false;
    });
};



// Render tags, linktags, with toggable subcribe button
var render_tags = function () {
    "use strict";

    $.each($('.ui-tag-link'), function() {

        var tag = $(this),
        toggle = tag.find('.ui-tag-link-toggle'),
        toggle_icon = toggle.attr('data-icon'),
        toggle_form = tag.find('.ui-tag-link-form'),
        toggle_url = toggle_form.attr('action');

        toggle.button({
            icons: {
                primary: toggle_icon
            },
            text: false
            }).click(function(event) {
            event.preventDefault();
            $.ajax({
                type: "POST",
                url: toggle_url,
                data: toggle_form.serialize(),
                statusCode: {
                    200: function(data) {
                        $.jGrowl(data.message);
                        if (data.tag_status === 1) {
                            $('.ui-tag-link-toggle[rel="' + toggle.attr('rel') + '"]').button("option", "icons", {
                                primary: 'ui-icon-star'
                            });

                        } else if (data.tag_status === 0) {
                            $('.ui-tag-link-toggle[rel="' + toggle.attr('rel') + '"]').button("option", "icons", {
                                primary: 'ui-icon-tag'
                            });
                        }

                    }
                }

            });

            return false;

        }).next().button().parent().buttonset();
    });
};

var preview_textarea = function(form, preview) {
    "use strict";

    var data = form.serialize() + "&preview=" + preview;

    $.ajax({
        type: "POST",
        url: '/utils/preview/',
        data: data,
        statusCode: {
            200: function(data) {

                var preview_modal = $('<div>' + data + '</div>');

                preview_modal.dialog({
                    width: 800,
                    modal: true,
                    position: ['center', 100],
                    title: 'Förhandsgranskning'
                    });

            }
        }
    });
};

var maximize_form = function(form_id, field_id) {
    "use strict";

    var oForm = $('#'+form_id),
        oTextarea = oForm.find('textarea[name='+field_id+']'),
        oField = oTextarea.parent(),
        win = oField.clone(),
        oText = oTextarea.val();

    var dialog = win.dialog({
        modal: true,
        position: ['center', 'left'],
        height: ( $(window).height()),
        width: ( $(window).width()),
        title: 'Storskärm',
        buttons: { 
                    "Kommentera": function() { 
                        win.dialog("close");
                        oForm.submit();
                    },
                    "Tillbaks": function() { 
                        win.dialog("close"); 
                    },
                    "Förhandsgranskning": function() {
                        oTextarea.val( win.find('textarea').val() );
                        preview_textarea( oForm, field_id);
                    }
                },
        draggable: false,
        beforeClose: function(event, ui) {
            oTextarea.val( win.find('textarea').val() );
            win.dialog( "destroy" );
        }
    }).parent().css({"position":"fixed","top":"0px"}).addClass('ui-state-maximized');

    dialog.find('textarea').css('height', ($(window).height()*0.8) ).val(oText);
    //dialog.find('.buttonset').hide();

};

var formatImageDialogs = function() {
    "use strict";
    $('.ui-widget-content .content img, .ui-text-panel img').attr('height', '80').unbind('click').click(function() {
        $(this).clone().dialog({
            resizable: false,
            modal: true,
            width: 'auto'
        });
    });
};

var formatJsReplyButton = function() {
    "use strict";
    $('.js-reply, .js-reply-all').button({
        icons: {
            primary: "ui-icon-comment"
        }
    });
};

// Cross Site Request Forgery protection 
$(document).ajaxSend(function(event, xhr, settings) {
    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = $.trim(cookies[i]);
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) == (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
    function sameOrigin(url) {
        // url could be relative or scheme relative or absolute
        var host = document.location.host; // host + port
        var protocol = document.location.protocol;
        var sr_origin = '//' + host;
        var origin = protocol + sr_origin;
        // Allow absolute or scheme relative URLs to same origin
        return (url == origin || url.slice(0, origin.length + 1) == origin + '/') ||
            (url == sr_origin || url.slice(0, sr_origin.length + 1) == sr_origin + '/') ||
            // or any other URL that isn't scheme relative or absolute i.e relative.
            !(/^(\/\/|http:|https:).*/.test(url));
    }
    function safeMethod(method) {
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }

    if (!safeMethod(settings.type) && sameOrigin(settings.url)) {
        xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
    }
});

/****************************************************************************************************************************************************
*
* Document Redy
*
*****************************************************************************************************************************************************/
$(document).ready(function() {
    "use strict";

    /*
    * Break out site from frames
    *
    */
    
    if (top !== self) {
        top.location.replace(self.location.href);
    }

    // Entry effekter
    $('.comment-entry').live('mouseenter', function(){
        $(this).removeClass( "comment-entry-mouseout" );
    });

    $('.comment-entry').live('mouseleave ', function(){
        $(this).addClass( "comment-entry-mouseout" );
    });
    
    // Render tags
    render_tags();

    // Hack for not allowing iframes to float over content.
    $("iframe").each(function(){
        var ifr_source = $(this).attr('src'),
            wmode = "wmode=transparent";
        if(ifr_source.indexOf('?') != -1) {
            var getQString = ifr_source.split('?'),
                oldString = getQString[1],
                newString = getQString[0];
            $(this).attr('src',newString+'?'+wmode+'&'+oldString);
        }
        else {
            $(this).attr('src',ifr_source+'?'+wmode);
        }
    });

    /*
    * Convaseation entry button for guestbooks
    *
    */
    $('.js-entry-conversation').button({
        icons: {
            primary: "ui-icon-transferthick-e-w"
        }
    });

    /*
    * Ajaxforms
    *
    */
    $('.ajax-delete-note').submit(function(event) {
        event.preventDefault();

        var form = $(this);

        $.ajax({
            type: "POST",
            url: form.attr('action'),
            data: form.serialize(),
            statusCode: {
                200: function() {
                    var anSelected = form.parents('tr');
                    $('#notification_table').dataTable().fnDeleteRow(anSelected[0]);

                    var number_of_notes = $('.ajax-delete-note').length;
                    $('#tab-counter-notes').html("(" + number_of_notes + ")");
                }
            }
        });

        return false;
    });

    /*
    * Tags
    * 
    */

    // Checkboxtags are toggleble tag buttons. Used when new entry are created.
    $('.ui-tag-edit input[type=checkbox]').button({
        icons: {
            primary: 'ui-icon-pencil'
        }
    });
    
    // Checkbox togglebutton
    $('.ui-toggle-button > input[type=checkbox]').button();

    //$('.ui-tag input[type=checkbox]').button( {icons: {primary:'ui-icon-tag'}});
    /*
    * Entrys
    *
    */
    formatImageDialogs();



    /*
    * jQuery UI accordions
    *
    */

    $('.accordion').accordion({
        collapsible: true,
        active: false,
        autoHeight: false
        });

    // Apply jQuery UI buttons
    $("input:submit, a.ui-button, button").button();
    $(".buttonset").buttonset();

    formatJsReplyButton();

    $("#account_button").button().next().button({
        text: false,
        icons: {
            primary: "ui-icon-gear"
        }
    }).unbind('click').click(function() {
        }).parent().buttonset();

    /*
    * Preview button for textareas
    *
    */
    $('input:[data-preview]').unbind('click').click(function() {
        var form = $(this).parentsUntil('form').parent();
        var preview = $(this).data('preview');
        preview_textarea(form, preview);
    });

    // Show messages with jGrowl
    var messages = $('.jGrowlmessages li, .errorlist li');
    messages.hide();
    messages.each(function() {
        $.jGrowl(this.innerHTML);
    });

    // User jQuery datepicker
    $(".datePicker").datepicker({
        yearRange: "-100:+0",
        dateFormat: 'yy-mm-dd',
        defaultDate: '-25y',
        changeYear: true,
        changeMonth: true

    });

    formatPagnation();


});

$(window).bind("load", function() {

    // THEMEROLLER
    $('#switcher').themeswitcher();

    // Hajlata enties
    highlightEntry();

    // Auto updater  
    if ( !$('body').hasClass('noupdate') ) {
        auto_update();
    }

});