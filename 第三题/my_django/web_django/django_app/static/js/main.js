;(function () {
	'use strict';
	var i = 0;
	$('.animate-box').waypoint( function( direction ) {
		if( direction === 'down' && !$(this.element).hasClass('animated-fast') ) {
			i++;
			$(this.element).addClass('item-animate');
			setTimeout(function(){
				$('body .animate-box.item-animate').each(function(k){
					var el = $(this);
					setTimeout( function () {
						var effect = el.data('animate-effect');
						el.addClass(effect + ' animated-fast');

						el.removeClass('item-animate');
					},  k * 200, 'easeInOutExpo' );
				});
			}, 100);
		}
	} , { offset: '85%' } );
}());

