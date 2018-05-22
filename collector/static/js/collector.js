


function prepare_ajax(){
  console.log("Preparing Ajax Setup");
  $.ajaxSetup({
    beforeSend: function(xhr, settings) {
      if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
        var csrf_middlewaretoken = $('input[name=csrfmiddlewaretoken]').val();        
        xhr.setRequestHeader("X-CSRFToken",csrf_middlewaretoken);
        //console.log("Cookie csrf:      "+csrftoken);
        console.log("Middleware csrf:  "+csrf_middlewaretoken);
      }
    }
  });
  }



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


$('#go').on('click',function(event){
  console.log($('.character_form').serialize());
  console.log($('.character_form input[name=cid]').val());
  var urlupdate = 'ajax/update/character/';
  $.ajax({    
    url: urlupdate,
    method: 'POST',
    headers: {
      'Accept': 'application/json',
      'Content-Type': 'application/x-www-form-urlencoded'
    },
    data: {
      cid: $('.character_form input[name=cid]').val(),
      character: $('.character_form').serialize(),
    },
    dataType: 'json',
    success: function(answer) {
        $(".details").html(answer);
        
        
      },
    error: function(answer) {
        $(".details").html(answer);
        
      },      
  });  
});

$('.view_character').on('click',function(event){
  event.preventDefault();
  $.ajax({
    url: 'ajax/view/character/'+$(this).attr('id')+'/',
    success: function(answer) {
        $(".details").html(answer)
      },
  });
});

$('.edit_character').on('click',function(event){
  event.preventDefault();
  $.ajax({
    url: 'ajax/edit/character/'+$(this).attr('id')+'/',
    success: function(answer) {
        $(".details").html(answer);
        prepare_ajax();        
    },
    error: function(answer){
      console.log('ooops... :(');
    }
  });
});




/* CSRF code on load */

/*
  function getCookie(name) {
    var cookieValue = null;
    var i = 0;
    if (document.cookie && document.cookie !== '') {
      var cookies = document.cookie.split(';');
      for (i; i < cookies.length; i++) {
        var cookie = jQuery.trim(cookies[i]);
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
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
  }

  $.ajaxSetup({
    crossDomain: false, // obviates need for sameOrigin test
    beforeSend: function(xhr, settings) {
      if (!csrfSafeMethod(settings.type)) {
        xhr.setRequestHeader("X-CSRFToken", csrftoken);
        console.log("Before send: token is: "+csrftoken);
      }
    }
  });
*/
  // https://www.djangoproject.com/weblog/2011/feb/08/security/
  
          



