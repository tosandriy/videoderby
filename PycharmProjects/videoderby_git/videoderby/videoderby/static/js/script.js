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
	slidesToShow: 6,
	slidesToScroll: 1,
	centerMode: false,
});

//$(".film-pages").slick({ //main page films pages
	//arrows: true,
	//dots: true,
	//speed: 1,
	//swipe: false,
	//slidesToShow: 4,
	//slidesToScroll: 4,
	//vertical: true,
	//customPaging : function(slider, i) {
	//var thumb = $(slider.$slides[i]).data();
	//return '<a>'+(i+1)+'</a>';
	//},
//});


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
	$('.slider-second .slick-active').eq(5).css({
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
	$('.actor_popular_works_slider .slick-active').eq(5).css({
		opacity: '0.4'
	});
	
}).trigger('afterChange');



$(".tab_item").not(":first").hide();
$(".film_trailer .tabBtn").click(function() {
	$(".film_trailer .tabBtn").removeClass("button_tab_active").eq($(this).index()).addClass("button_tab_active");
	$(".tab_item").hide().eq($(this).index()).fadeIn()
}).eq(0);


$(document).ready(function(){
	list1=$(".review")
	for (i = 0; i < list1.length; i++) {
		review_t = $(list1[i]).children(".review_t").height()
		review_t1 = $(list1[i]).children(".review_t").children(".review_container").height()
		if (review_t1>review_t) {
			//$(list1[i]).children(".review_t").height(review_t1)
			$(list1[i]).children(".review_footer").children(".show_all_review").css("display","block")
		}
	}
})
function openCom(x) {
	scrollPos = $(window).scrollTop()
	$(x).parent().parent().children(".review_t").toggleClass("close")
	$(x).hide()
	$(x).parent().children(".close_all_review").show()
	$(window).scrollTop(scrollPos) 
	//h = $(x).parent().parent().children(".review_t").height()
	//$(x).parent().parent().children(".review_t").css("height","auto")
	//h2 = $(x).parent().parent().children(".review_t").height()
	//$(x).parent().parent().children(".review_t").css("height",h)
	//$(x).parent().parent().children(".review_t").animate({height:h2})
	//console.log($(this).parent().parent().children(".review_t"))
}
function closeCom(x) {
	scrollPos = $(window).scrollTop()
	$(x).parent().parent().children(".review_t").toggleClass("close")
	$(x).hide()
	$(x).parent().children(".show_all_review").show()
	$(window).scrollTop(scrollPos) 
}
$(".films_select").click(function(){
	list1 = $(".films_select")
	for (i = 0; i < list1.length; i++) {
		if (!$(list1[i]).is(this)){
			$(list1[i]).removeClass("films_select_open")
			$(list1[i]).parent().children(".select_list").removeClass("list-open")
		}
	}
	$(this).toggleClass("films_select_open")
	$(this).parent().children(".select_list").toggleClass("list-open")
})
$(document).mouseup(function (e){ 
	var div = $(".films_select"); 
	var div2 = $(".select_list_item");
	if (!div.is(e.target) && div.has(e.target).length === 0 && !div2.is(e.target) && div2.has(e.target).length === 0) {
		$(".films_select").removeClass("films_select_open")
		$(".select_list").removeClass("list-open")
	}
});
// $(".select_list_item").children("label").click(function(){
// 	$(".films_select").removeClass("films_select_open")
// 	$(".select_list").removeClass("list-open")
// })
$(window).on("load",function(){
	$(".select_list").mCustomScrollbar({
		scrollInertia:300
	});
});
$('.review_star').raty({
	number: 10,
	starOn: '/static/images/staron.png',
	starOff: '/static/images/staroff.png'
})

$('.user_fav').click(function(){
	$('.fav_content').toggleClass('user_active')
})
$('.password_change').click(function(){
	$('.password_change_form').addClass('user_active')
	var docHeight = $(document).height();
   	$("body").append("<div class='overlay'></div>");
   	$(".overlay")
      	.height(docHeight)
      	.css({
         	'opacity' : 0.4,
         	'position': 'absolute',
         	'top': 0,
         	'left': 0,
         	'background-color': 'black',
         	'width': '100%',
         	'z-index': 5000
      	});
    $(".overlay").on("click", function () {
		$(".overlay").remove()
		$('.password_change_form').removeClass('user_active')
	})
});
$('.email_change').click(function(){
	$('.email_change_form').addClass('user_active')
	var docHeight = $(document).height();
   	$("body").append("<div class='overlay'></div>");
   	$(".overlay")
      	.height(docHeight)
      	.css({
         	'opacity' : 0.4,
         	'position': 'absolute',
         	'top': 0,
         	'left': 0,
         	'background-color': 'black',
         	'width': '100%',
         	'z-index': 5000
      	});
    $(".overlay").on("click", function () {
		$(".overlay").remove()
		$('.email_change_form').removeClass('user_active')
	})
});
$('.user_img_change').click(function(){
	$('.img_change_form').addClass('user_active')
	var docHeight = $(document).height();
   	$("body").append("<div class='overlay'></div>");
   	$(".overlay")
      	.height(docHeight)
      	.css({
         	'opacity' : 0.4,
         	'position': 'absolute',
         	'top': 0,
         	'left': 0,
         	'background-color': 'black',
         	'width': '100%',
         	'z-index': 5000
      	});
    $(".overlay").on("click", function () {
		$(".overlay").remove()
		$('.img_change_form').removeClass('user_active')
	})
});
$('.user_name_change').click(function(){
	$('.nick_change_form').addClass('user_active')
	var docHeight = $(document).height();
   	$("body").append("<div class='overlay'></div>");
   	$(".overlay")
      	.height(docHeight)
      	.css({
         	'opacity' : 0.4,
         	'position': 'absolute',
         	'top': 0,
         	'left': 0,
         	'background-color': 'black',
         	'width': '100%',
         	'z-index': 5000
      	});
    $(".overlay").on("click", function () {
		$(".overlay").remove()
		$('.nick_change_form').removeClass('user_active')
	})
});

// window.onload = function() {
// 	var errorList = $('<div class="messeges"></div>')
// 	errorList.appendTo('body')
// }
// function errorMes(text, type) {
// 	if (type == 'succes') {
// 		var $newError = $("<div class='messege succes'><p class='messege_text'></p></div>")
// 	}
// 	else if (type == 'error') {
// 		var $newError = $("<div class='messege error'><p class='messege_text'></p></div>")
// 	}
// 	$newError.appendTo(".messeges")
// 	var errorWindow = $('.messege')
// 	var errorText = $('.messege_text')
// 	errorText.text(text);
// 	errorWindow.delay(2000).fadeOut(1000);
// }
function errorMes(text, heading, icon) {
	$.toast({
	    heading: heading, //Принимает:  Information, Error, Warning, Success
	    text: text, //текст
	    loader: true, // есть ли убывающая линия
	    loaderBg: '#9EC600', // бг для убывающей линии
	    icon: icon //Принимает:  info, error, warning, success
	})
}

$(document).on('click', '.notifBtn',function() {
	if ($('.notifList').css('display') == 'none') {
		$('.notifList').show(400)
	}
	else {
		$('.notifList').hide(400)
		var elems = document.getElementsByClassName('newNotif');
            for(var i=0; i < elems.length; i++) {
                elems[i].className = 'notifNote';
                }
	}
})
$(document).mouseup(function (e){ 
	var div = $(".notifList"); 
	if (!div.is(e.target) && div.has(e.target).length === 0) {
		$(".notifList").hide(400)
		if ($('.notifList').css('display') != 'none') {
		var elems = document.getElementsByClassName('newNotif');
            for(var i=0; i < elems.length; i++) {
                elems[i].className = 'notifNote';
                }
	}

	}
});

$('.slider_frame').click(function(){
	var docHeight = $(document).height();
	$("body").append("<div class='overlay'></div>");
	$(".overlay")
	    .height(docHeight)
	    .css({
	        'opacity' : 0.4,
	        'position': 'absolute',
	        'top': 0,
	        'left': 0,
	        'background-color': 'black',
	        'width': '100%',
	        'z-index': 5000
	    });
	$(".overlay").on("click", function () {
		$(".overlay").remove()
		$('.imgShow').remove()
	})
	$(document).on("click", '.imgShow', function () {
		$(".overlay").remove()
		$('.imgShow').remove()
	})
	$(this).clone().toggleClass('imgShow').removeClass('slick-slide').removeClass('slick-active').css({
		'position':'fixed',
		'z-index': 5001,
		'top': '50%',
		'left': '50%',
        'transform': 'translate(-50%, -50%)',
        'transform': 'scale(3)',
        'margin-left': '-100px',
	}).appendTo('body');
})


