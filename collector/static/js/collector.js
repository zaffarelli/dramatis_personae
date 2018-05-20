


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

$('.view_character').on('click',function(event){  
  event.preventDefault();
  $.ajax({
    url: 'ajax/view/character/'+$(this).attr('id')+'/',
    success: function(answer) {
        $(".details").html(answer)
      },
  });
})

 // CSRF code
function getCookie(name) {
  var cookieValue = null;
  var i = 0;
  if (document.cookie && document.cookie !== '') {
    var cookies = document.cookie.split(';');
    for (i; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
    var csrftoken = getCookie('csrftoken');

    function csrfSafeMethod(method) {
        // these HTTP methods do not require CSRF protection
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }
    $.ajaxSetup({
        crossDomain: false, // obviates need for sameOrigin test
        beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type)) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    }); 
