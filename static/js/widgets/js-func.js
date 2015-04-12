$(function(){ 
	
	//PNG fix for IE6
	if($.browser.msie && $.browser.version.substr(0,1) == 6){
		DD_belatedPNG.fix('.overlay, .mark-featured');
	}
	
	//Blink Fields
	 $('.blink').
	    focus(function() {
	        if(this.title==this.value) {
	            this.value = '';
	        }
	    }).
	    blur(function(){
	        if(this.value=='') {
	            this.value = this.title;
	        }
	    });
	    
	//Overlay Hover
	$('.box-image').hover(function(){ 
		$('.overlay', this).toggle();
	 });
	 
	 //Hide Box
	 $(".close").click(function(){ 
	 	$(this).parent().fadeOut('fast');
	 	return false;
  	});
  	
  	//FancyBox
	$(".overlay").fancybox({
		'transitionIn'	: 'elastic',
		'transitionOut'	: 'elastic',
		'easingIn'      : 'easeOutBack',
		'easingOut'     : 'easeInBack',
		'overlayColor'	: '#000',
		'overlayOpacity' : '0.7'
	});
	
	//Tabs
	$('.tabs li a').click(function(){ 
		$('.tabs li a').removeClass('active');
		$(this).addClass('active');
		var href = $(this).attr('href');
		$('.tabs-list').hide();
		$(href).show();
		return false;
	 });
	
});