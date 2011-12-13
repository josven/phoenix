
// usage: log('inside coolFunc', this, arguments);
// paulirish.com/2009/log-a-lightweight-wrapper-for-consolelog/
window.log = function(){
  log.history = log.history || [];   // store logs to an array for reference
  log.history.push(arguments);
  if(this.console) {
    arguments.callee = arguments.callee.caller;
    var newarr = [].slice.call(arguments);
    (typeof console.log === 'object' ? log.apply.call(console.log, console, newarr) : console.log.apply(console, newarr));
  }
};

// make it safe to use console.log always
(function(b){function c(){}for(var d="assert,count,debug,dir,dirxml,error,exception,group,groupCollapsed,groupEnd,info,log,timeStamp,profile,profileEnd,time,timeEnd,trace,warn".split(","),a;a=d.pop();){b[a]=b[a]||c}})((function(){try
{console.log();return window.console;}catch(err){return window.console={};}})());


// place any jQuery/helper plugins in here, instead of separate, slower script files.

// jQuery Growl - https://bitbucket.org/stanlemon/jgrowl/raw/ff9e18fcc827/jquery.jgrowl_minimized.js
(function($){$.jGrowl=function(m,o){if($('#jGrowl').size()==0)
$('<div id="jGrowl"></div>').addClass((o&&o.position)?o.position:$.jGrowl.defaults.position).appendTo('body');$('#jGrowl').jGrowl(m,o);};$.fn.jGrowl=function(m,o){if($.isFunction(this.each)){var args=arguments;return this.each(function(){var self=this;if($(this).data('jGrowl.instance')==undefined){$(this).data('jGrowl.instance',$.extend(new $.fn.jGrowl(),{notifications:[],element:null,interval:null}));$(this).data('jGrowl.instance').startup(this);}
if($.isFunction($(this).data('jGrowl.instance')[m])){$(this).data('jGrowl.instance')[m].apply($(this).data('jGrowl.instance'),$.makeArray(args).slice(1));}else{$(this).data('jGrowl.instance').create(m,o);}});};};$.extend($.fn.jGrowl.prototype,{defaults:{pool:0,header:'',group:'',sticky:false,position:'top-right',glue:'after',theme:'default',themeState:'highlight',corners:'10px',check:250,life:3000,closeDuration:'normal',openDuration:'normal',easing:'swing',closer:true,closeTemplate:'&times;',closerTemplate:'<div>[ close all ]</div>',log:function(e,m,o){},beforeOpen:function(e,m,o){},afterOpen:function(e,m,o){},open:function(e,m,o){},beforeClose:function(e,m,o){},close:function(e,m,o){},animateOpen:{opacity:'show'},animateClose:{opacity:'hide'}},notifications:[],element:null,interval:null,create:function(message,o){var o=$.extend({},this.defaults,o);if(typeof o.speed!=='undefined'){o.openDuration=o.speed;o.closeDuration=o.speed;}
this.notifications.push({message:message,options:o});o.log.apply(this.element,[this.element,message,o]);},render:function(notification){var self=this;var message=notification.message;var o=notification.options;var notification=$('<div class="jGrowl-notification '+o.themeState+' ui-corner-all'+
((o.group!=undefined&&o.group!='')?' '+o.group:'')+'">'+'<div class="jGrowl-close">'+o.closeTemplate+'</div>'+'<div class="jGrowl-header">'+o.header+'</div>'+'<div class="jGrowl-message">'+message+'</div></div>').data("jGrowl",o).addClass(o.theme).children('div.jGrowl-close').bind("click.jGrowl",function(){$(this).parent().trigger('jGrowl.close');}).parent();$(notification).bind("mouseover.jGrowl",function(){$('div.jGrowl-notification',self.element).data("jGrowl.pause",true);}).bind("mouseout.jGrowl",function(){$('div.jGrowl-notification',self.element).data("jGrowl.pause",false);}).bind('jGrowl.beforeOpen',function(){if(o.beforeOpen.apply(notification,[notification,message,o,self.element])!=false){$(this).trigger('jGrowl.open');}}).bind('jGrowl.open',function(){if(o.open.apply(notification,[notification,message,o,self.element])!=false){if(o.glue=='after'){$('div.jGrowl-notification:last',self.element).after(notification);}else{$('div.jGrowl-notification:first',self.element).before(notification);}
$(this).animate(o.animateOpen,o.openDuration,o.easing,function(){if($.browser.msie&&(parseInt($(this).css('opacity'),10)===1||parseInt($(this).css('opacity'),10)===0))
this.style.removeAttribute('filter');$(this).data("jGrowl").created=new Date();$(this).trigger('jGrowl.afterOpen');});}}).bind('jGrowl.afterOpen',function(){o.afterOpen.apply(notification,[notification,message,o,self.element]);}).bind('jGrowl.beforeClose',function(){if(o.beforeClose.apply(notification,[notification,message,o,self.element])!=false)
$(this).trigger('jGrowl.close');}).bind('jGrowl.close',function(){$(this).data('jGrowl.pause',true);$(this).animate(o.animateClose,o.closeDuration,o.easing,function(){$(this).remove();var close=o.close.apply(notification,[notification,message,o,self.element]);if($.isFunction(close))
close.apply(notification,[notification,message,o,self.element]);});}).trigger('jGrowl.beforeOpen');if(o.corners!=''&&$.fn.corner!=undefined)$(notification).corner(o.corners);if($('div.jGrowl-notification:parent',self.element).size()>1&&$('div.jGrowl-closer',self.element).size()==0&&this.defaults.closer!=false){$(this.defaults.closerTemplate).addClass('jGrowl-closer ui-state-highlight ui-corner-all').addClass(this.defaults.theme).appendTo(self.element).animate(this.defaults.animateOpen,this.defaults.speed,this.defaults.easing).bind("click.jGrowl",function(){$(this).siblings().trigger("jGrowl.beforeClose");if($.isFunction(self.defaults.closer)){self.defaults.closer.apply($(this).parent()[0],[$(this).parent()[0]]);}});};},update:function(){$(this.element).find('div.jGrowl-notification:parent').each(function(){if($(this).data("jGrowl")!=undefined&&$(this).data("jGrowl").created!=undefined&&($(this).data("jGrowl").created.getTime()+parseInt($(this).data("jGrowl").life))<(new Date()).getTime()&&$(this).data("jGrowl").sticky!=true&&($(this).data("jGrowl.pause")==undefined||$(this).data("jGrowl.pause")!=true)){$(this).trigger('jGrowl.beforeClose');}});if(this.notifications.length>0&&(this.defaults.pool==0||$(this.element).find('div.jGrowl-notification:parent').size()<this.defaults.pool))
this.render(this.notifications.shift());if($(this.element).find('div.jGrowl-notification:parent').size()<2){$(this.element).find('div.jGrowl-closer').animate(this.defaults.animateClose,this.defaults.speed,this.defaults.easing,function(){$(this).remove();});}},startup:function(e){this.element=$(e).addClass('jGrowl').append('<div class="jGrowl-notification"></div>');this.interval=setInterval(function(){$(e).data('jGrowl.instance').update();},parseInt(this.defaults.check));if($.browser.msie&&parseInt($.browser.version)<7&&!window["XMLHttpRequest"]){$(this.element).addClass('ie6');}},shutdown:function(){$(this.element).removeClass('jGrowl').find('div.jGrowl-notification').remove();clearInterval(this.interval);},close:function(){$(this.element).find('div.jGrowl-notification').each(function(){$(this).trigger('jGrowl.beforeClose');});}});$.jGrowl.defaults=$.fn.jGrowl.prototype.defaults;})(jQuery);

/*
 * jQuery.fn.autoResize 1.14
 * --
 * https://github.com/jamespadolsey/jQuery.fn.autoResize
 * --
 * This program is free software. It comes without any warranty, to
 * the extent permitted by applicable law. You can redistribute it
 * and/or modify it under the terms of the Do What The Fuck You Want
 * To Public License, Version 2, as published by Sam Hocevar. See
 * http://sam.zoy.org/wtfpl/COPYING for more details. */ 

(function($){

	var uid = 'ar' + +new Date,

		defaults = autoResize.defaults = {
			onResize: function(){},
			onBeforeResize: function(){return 123},
			onAfterResize: function(){return 555},
			animate: {
				duration: 200,
				complete: function(){}
			},
			extraSpace: 50,
			minHeight: 'original',
			maxHeight: 500,
			minWidth: 'original',
			maxWidth: 500
		};

	autoResize.cloneCSSProperties = [
		'lineHeight', 'textDecoration', 'letterSpacing',
		'fontSize', 'fontFamily', 'fontStyle', 'fontWeight',
		'textTransform', 'textAlign', 'direction', 'wordSpacing', 'fontSizeAdjust',
		'paddingTop', 'paddingLeft', 'paddingBottom', 'paddingRight', 'width'
	];

	autoResize.cloneCSSValues = {
		position: 'absolute',
		top: -9999,
		left: -9999,
		opacity: 0,
		overflow: 'hidden'
	};

	autoResize.resizableFilterSelector = [
		'textarea:not(textarea.' + uid + ')',
		'input:not(input[type])',
		'input[type=text]',
		'input[type=password]',
		'input[type=email]',
		'input[type=url]'
	].join(',');

	autoResize.AutoResizer = AutoResizer;

	$.fn.autoResize = autoResize;

	function autoResize(config) {
		this.filter(autoResize.resizableFilterSelector).each(function(){
			new AutoResizer( $(this), config );
		});
		return this;
	}

	function AutoResizer(el, config) {

		if (el.data('AutoResizer')) {
			el.data('AutoResizer').destroy();
		}
		
		config = this.config = $.extend({}, autoResize.defaults, config);
		this.el = el;

		this.nodeName = el[0].nodeName.toLowerCase();

		this.originalHeight = el.height();
		this.previousScrollTop = null;

		this.value = el.val();

		if (config.maxWidth === 'original') config.maxWidth = el.width();
		if (config.minWidth === 'original') config.minWidth = el.width();
		if (config.maxHeight === 'original') config.maxHeight = el.height();
		if (config.minHeight === 'original') config.minHeight = el.height();

		if (this.nodeName === 'textarea') {
			el.css({
				resize: 'none',
				overflowY: 'hidden'
			});
		}

		el.data('AutoResizer', this);

		// Make sure onAfterResize is called upon animation completion
		config.animate.complete = (function(f){
			return function() {
				config.onAfterResize.call(el);
				return f.apply(this, arguments);
			};
		}(config.animate.complete));

		this.bind();

	}

	AutoResizer.prototype = {

		bind: function() {

			var check = $.proxy(function(){
				this.check();
				return true;
			}, this);

			this.unbind();

			this.el
				.bind('keyup.autoResize', check)
				//.bind('keydown.autoResize', check)
				.bind('change.autoResize', check)
				.bind('paste.autoResize', function() {
					setTimeout(function() { check(); }, 0);
				});
			
			if (!this.el.is(':hidden')) {
				this.check(null, true);
			}

		},

		unbind: function() {
			this.el.unbind('.autoResize');
		},

		createClone: function() {

			var el = this.el,
				clone = this.nodeName === 'textarea' ? el.clone() : $('<span/>');

			this.clone = clone;

			$.each(autoResize.cloneCSSProperties, function(i, p){
				clone[0].style[p] = el.css(p);
			});

			clone
				.removeAttr('name')
				.removeAttr('id')
				.addClass(uid)
				.attr('tabIndex', -1)
				.css(autoResize.cloneCSSValues);

			if (this.nodeName === 'textarea') {
				clone.height('auto');
			} else {
				clone.width('auto').css({
					whiteSpace: 'nowrap'
				});
			}

		},

		check: function(e, immediate) {

			if (!this.clone) {
		this.createClone();
		this.injectClone();
			}

			var config = this.config,
				clone = this.clone,
				el = this.el,
				value = el.val();

			// Do nothing if value hasn't changed
			if (value === this.prevValue) { return true; }
			this.prevValue = value;

			if (this.nodeName === 'input') {

				clone.text(value);

				// Calculate new width + whether to change
				var cloneWidth = clone.width(),
					newWidth = (cloneWidth + config.extraSpace) >= config.minWidth ?
						cloneWidth + config.extraSpace : config.minWidth,
					currentWidth = el.width();

				newWidth = Math.min(newWidth, config.maxWidth);

				if (
					(newWidth < currentWidth && newWidth >= config.minWidth) ||
					(newWidth >= config.minWidth && newWidth <= config.maxWidth)
				) {

					config.onBeforeResize.call(el);
					config.onResize.call(el);

					el.scrollLeft(0);

					if (config.animate && !immediate) {
						el.stop(1,1).animate({
							width: newWidth
						}, config.animate);
					} else {
						el.width(newWidth);
						config.onAfterResize.call(el);
					}

				}

				return;

			}

			// TEXTAREA
			
			clone.width(el.width()).height(0).val(value).scrollTop(10000);
			
			var scrollTop = clone[0].scrollTop;
				
			// Don't do anything if scrollTop hasen't changed:
			if (this.previousScrollTop === scrollTop) {
				return;
			}

			this.previousScrollTop = scrollTop;
			
			if (scrollTop + config.extraSpace >= config.maxHeight) {
				el.css('overflowY', '');
				scrollTop = config.maxHeight;
				immediate = true;
			} else if (scrollTop <= config.minHeight) {
				scrollTop = config.minHeight;
			} else {
				el.css('overflowY', 'hidden');
				scrollTop += config.extraSpace;
			}

			config.onBeforeResize.call(el);
			config.onResize.call(el);

			// Either animate or directly apply height:
			if (config.animate && !immediate) {
				el.stop(1,1).animate({
					height: scrollTop
				}, config.animate);
			} else {
				el.height(scrollTop);
				config.onAfterResize.call(el);
			}

		},

		destroy: function() {
			this.unbind();
			this.el.removeData('AutoResizer');
			this.clone.remove();
			delete this.el;
			delete this.clone;
		},

		injectClone: function() {
			(
				autoResize.cloneContainer ||
				(autoResize.cloneContainer = $('<arclones/>').appendTo('body'))
			).append(this.clone);
		}

	};
	
})(jQuery);