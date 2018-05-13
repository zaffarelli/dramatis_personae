


$(window).scroll(function(){
  var sticky = $('.menu'), scroll = $(window).scrollTop(), wrap = $('.wrapper');
  if (scroll >= 100){
    sticky.addClass('fixed');
    wrap.addClass('stickyoffset');
  }else{
    sticky.removeClass('fixed');
    wrap.removeClass('stickyoffset');
  }
});
