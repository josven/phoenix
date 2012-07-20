// Formatera jQuery UI för denna app
var formatjQueryUI = function() {
    $('input:submit, a.ui-button, button').button();
    $('.buttonset').buttonset();
};

jQuery(document).ready(function() {

    // Formatera jQuery UI grejer efter ajaxComplete
    $('body').ajaxComplete(function() {
        formatjQueryUI();
    });

	// Visa kommentarer
	$('.js-show-comments').click(function(event) {
		event.preventDefault();
		
		var button = $(this),
			loader = $('&nbsp;<img src="/static/img/ajax-loader.gif" class="gif-submit-loader" alt="Wakawakawakawakawaka..." />');

		button.parent().after( loader );
		button.addClass('ui-state-active');

		var btn = $(this),
			url = btn.data('url'),
			cont = $('#'+btn.data('container') );
		 
		cont.load(url, function(){
			loader.remove();
			button.removeClass('ui-state-active');
		});

		return false;
	});
});