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
	// prevArrow: '<img src="images/vectors/ArrowLeft.png" class="prevArrow">',
	// nextArrow: '<img src="images/vectors/ArrowRight.png" class="nextArrow">'
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