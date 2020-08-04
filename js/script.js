$(".slider-first").slick({ //Top Slider
	arrows: false,
	dots: true,
	infinite: true,
	vertical: false,
	speed: 1000,
	autoplay:true,
	autoplaySpeed: 4000,
	swipe: true,
	pauseOnDotsHover: true
});
$(".slider-second").slick({ //slider with films
	arrows: true,
	dots: false,
	infinite: true,
	vertical: false,
	speed: 500,
	autoplay:false,
	swipe: true,
	slidesToShow: 7,
	slidesToScroll: 1,
	centerMode: false,
});

$(".film-pages").slick({ //main page films pages
	arrows: true,
	dots: true,
	speed: 1,
	swipe: false,
	slidesToShow: 4,
	slidesToScroll: 4,
	vertical: true,
	customPaging : function(slider, i) {
	var thumb = $(slider.$slides[i]).data();
	return '<a>'+(i+1)+'</a>';
	},
});


$(".actor_photos_slider").slick({ //slider with actor photos
	arrows: true,
	dots: false,
	infinite: true,
	vertical: false,
	speed: 1000,
	autoplay:false,
	swipe: true,
	slidesToShow: 1,
	slidesToScroll: 1,
	centerMode: false,
});
$(".actor_popular_works_slider").slick({ //slider with actor popular works
	arrows: true,
	dots: false,
	infinite: true,
	vertical: false,
	speed: 500,
	autoplay:false,
	swipe: true,
	slidesToShow: 7,
	slidesToScroll: 1,
	centerMode: false,
});

$(".film_frames_slider").slick({ //slider with film frames
	arrows: true,
	dots: false,
	infinite: true,
	vertical: false,
	speed: 500,
	autoplay:false,
	swipe: true,
	slidesToShow: 4,
	slidesToScroll: 1,
	centerMode: false,
});

$('.slider-second').on('afterChange', function(event, slick, currentSlide, nextSlide){

	$('.slider-second .slick-slide').css({
		opacity: '0.2'
	});
	$('.slider-second .slick-active').css({
		opacity: '1'
	});
	$('.slider-second .slick-active').eq(0).css({
		opacity: '0.4'
	});
	$('.slider-second .slick-active').eq(6).css({
		opacity: '0.4'
	});
	
}).trigger('afterChange');

$('.actor_popular_works_slider').on('afterChange', function(event, slick, currentSlide, nextSlide){

	$('.actor_popular_works_slider .slick-slide').css({
		opacity: '0.2'
	});
	$('.actor_popular_works_slider .slick-active').css({
		opacity: '1'
	});
	$('.actor_popular_works_slider .slick-active').eq(0).css({
		opacity: '0.4'
	});
	$('.actor_popular_works_slider .slick-active').eq(6).css({
		opacity: '0.4'
	});
	
}).trigger('afterChange');



function openTab(evt, tabName) {
	var i, x, tablinks;
	x = document.getElementsByClassName("tab");
	for (i = 0; i < x.length; i++) {
	    x[i].style.display = "none";
	}
	tablinks = document.getElementsByClassName("tabBtn");
	for (i = 0; i < x.length; i++) {
	    tablinks[i].className = tablinks[i].className.replace(" button_tab_active", "");
	}
	document.getElementById(tabName).style.display = "flex";
	evt.currentTarget.className += " button_tab_active"; 
}


$('.review_star').raty({
	number: 5,
	starOn: 'images/vectors/staron.png',
	starOff: 'images/vectors/staroff.png'
})