/*
 ╔╦╗╔═╗  ╔═╗┌─┐┬  ┬  ┌─┐┌─┐┌┬┐┌─┐┬─┐
  ║║╠═╝  ║  │ ││  │  ├┤ │   │ │ │├┬┘
 ═╩╝╩    ╚═╝└─┘┴─┘┴─┘└─┘└─┘ ┴ └─┘┴└─
*/
function prepare_ajax(){
  $.ajaxSetup({
    beforeSend: function(xhr, settings) {
      if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
        var csrf_middlewaretoken = $('input[name=csrfmiddlewaretoken]').val();        
        xhr.setRequestHeader('X-CSRFToken',csrf_middlewaretoken);
      }
    }
  });
  /*
    

  */
  
}

// Chart event handler
function keywordHandlerClick(evt) {
    var firstPoint = chart_keywords.getElementAtEvent(evt)[0];
    if (firstPoint) {
        var label = chart_keywords.data.labels[firstPoint._index];
        var value = chart_keywords.data.datasets[firstPoint._datasetIndex].data[firstPoint._index];        
        $('#customize').val(label);
        $('#search.btn').click();
    }
}

function loadKeywords(){
  $.ajax({
    url: 'api/keywords/',
    success: function(answer) {
      $('#keywords').html('')
      $('#keywords').append(answer.chart);
      rebootlinks();
    },
  });
}



function register_story(x){
  $('.view_'+x).off();
  $('.view_'+x).on('click', function(event){
    event.preventDefault();
    event.stopPropagation();
    t_id = $(this).attr('id')
    $.ajax({
      url: x+'s/'+t_id+'/view',
      success: function(answer) {
        $('#'+x+'_'+t_id).html(answer);        
        prepare_ajax();
        rebootlinks();
      },
      error: function(answer){
        console.log('ooops... on view '+x+' :(');
      }
    });
  });

  $('.hide_'+x).off();
  $('.hide_'+x).on('click', function(event){
    event.preventDefault();
    event.stopPropagation();
    t_id = $(this).attr('id')
    $('#'+x+'_'+t_id).html('');
    prepare_ajax();
    rebootlinks();
  });

  $('.edit_'+x).off();
  $('.edit_'+x).on('click', function(event){
    event.preventDefault();
    event.stopPropagation();
    t_id = $(this).attr('id')
    $.ajax({
      url: x+'s/'+t_id+'/edit',
      success: function(answer) {
        $('#'+x+'_'+t_id).html(answer);        
        prepare_ajax();
        rebootlinks();
      },
      error: function(answer){
        console.log('ooops... on edit '+x+':(');
      }
    });
  });



  $('.'+x+'_update').off();
  $('.'+x+'_update').on('click',function(event){
    event.preventDefault();
    event.stopPropagation();    
    var owner = $(this).closest('div.storyarticle').attr('id');
    var id = $(this).closest('div.storyarticle').attr('id').split('_')[1];
    var form = $(this).closest('form');
    formdata = form.serialize();
    var urlupdate = x+'s/'+id+'/edit';    
    $.ajax({    
      url: urlupdate,
      method: 'POST',
      headers: {
        'Accept': 'application/json',
        'Content-Type': 'application/x-www-form-urlencoded'
      },
      data: formdata,
      dataType: 'json',
      success: function(answer) {
        console.log('Success... ');
        $('#'+owner).html(answer);
        rebootlinks();
        $('button#'+id+'.view_'+x).click();
      },
      error: function(answer) {
        console.log('Error... ');
        console.log(answer);
      },
    });  
  });

  $('.add_'+x).off();
  $('.add_'+x).on('click',function(event){
    event.preventDefault();
    event.stopPropagation();
    var id = $(this).parent('p').prop('className');
    console.log(id);    
    //var form = $(this).closest('form');
    var urlupdate = x+'s/add';    
    $.ajax({    
      url: urlupdate,
      method: 'POST',
      headers: {
        'Accept': 'application/json',
        'Content-Type': 'application/x-www-form-urlencoded'
      },
      data: {'id': id},
      dataType: 'json',
      success: function(answer) {
        console.log('Success... ');
        console.log(id);
        //$('#'+id).html(answer);
        rebootlinks();
        //$('button#'+id+'.view_'+x).click();
      },
      error: function(answer) {
        console.log('Error... ');
        console.log(answer);
      },
    });  
  });


  
}

function update_messenger(){
    $.ajax({
      url: 'ajax/messenger/',
      success: function(answer) {
        $('#messenger').html(answer)
      },
    });
}

  
function loadajax(){
    $.ajax({
      url: 'ajax/storyline/none/',
      success: function(answer) {
        $('.storyline').html(answer)
        $.ajax({
          url: 'ajax/list/none/1/',
          success: function(answer) {
            $('.charlist').html(answer)
            rebootlinks();
          },
        });
      },
    });
}


function rebootlinks(){

  
  
  
  $('.nav').off();
  $('.nav').on('click',function(event){
    event.preventDefault();
    event.stopPropagation();
    key = $('#customize').val(); 
    if (key == ''){
      key='none';
    }
    $.ajax({
      url: 'ajax/list/'+key+'/'+$(this).attr('page')+'/',
      success: function(answer) {
        $('.charlist').html(answer)
        rebootlinks();
      },
    });   
  });

  $('.episode_cast').off();
  $('.episode_cast').on('click',function(event){
    event.preventDefault();
    event.stopPropagation();
    slug = $(this).attr('id');
    $('#customize').val(slug); 
    $.ajax({
      url: 'ajax/list/'+slug+'/'+$(this).attr('page')+'/',
      success: function(answer) {
        $('.charlist').html(answer)
        rebootlinks();
      },
    });   
  });


  $('#current_storyline').off();
  $('#current_storyline').on('change',function(event){
    event.preventDefault();
    event.stopPropagation();
    slug = $('#current_storyline').val();
    console.log(slug);
    $.ajax({      
      url: 'ajax/storyline/'+slug+'/',
      success: function(answer) {
        $('.storyline').html(answer)
        $.ajax({
          url: 'ajax/list/none/1/',
          success: function(answer) {
            $('.charlist').html(answer)
            rebootlinks();
          },
        });
      },
    });
  });


  $('#popstats').off();
  $('#popstats').on('click',function(event){
    event.preventDefault();
    event.stopPropagation();
    $.ajax({
      url: 'api/popstats/',
      success: function(answer) {
        //console.log(answer.chart1);
        $('.details').html('')
        answer.charts.forEach(function(elem){
          $('.details').append(elem);
        });
        rebootlinks();
        update_messenger();
      },
    });
    rebootlinks();
  });

  


  $(window).scroll(function(){
    var sticky = $('.menu'), scroll = $(window).scrollTop(), wrap = $('.wrapper');
    if (scroll >= 105){
      sticky.addClass('fixed');
      wrap.addClass('stickyoffset');
    }else{
      sticky.removeClass('fixed');
      wrap.removeClass('stickyoffset');
    }
  });

  /* Character Edition & Update*/
  $('.edit_character').off();
  $('.edit_character').on('click',function(event){
    event.preventDefault();
    event.stopPropagation();
    var dad = $(this).parents('li').find('div.avatar_link');
    $('li').find('div.avatar_link').removeClass('selected');
    $(dad).addClass('selected');
    $('body').toggleClass('waiting');
    $.ajax({
      url: 'characters/'+$(this).attr('id')+'/edit/',
      success: function(answer) {
        $('.details').html(answer);
        $('body').toggleClass('waiting');
        prepare_ajax();
        loadKeywords();
        rebootlinks();
        update_messenger();
      },
      error: function(answer){
        console.log('ooops... :(');
        update_messenger();
      }
    });
  });

  $('#go').off();
  $('#go').on('click',function(event){
    event.preventDefault();
    event.stopPropagation();
    var formdata = $('.character_form').serialize();
    var id = $('.character_form input[name=id]').val();
    var rid = $('.character_form input[name=rid]').val();
    $.ajax({
      url: 'characters/'+id+'/edit/',
      method: 'POST',      
      headers: {
        'Accept': 'application/json',
        'Content-Type': 'application/x-www-form-urlencoded'
        },
      data: formdata,
      dataType: 'json',
      success: function(answer) {
          $('li').find('div.avatar_link').removeClass('selected');
          $('li').find('div.avatar_link').find('#'+id+'.view_character').click();
          rebootlinks();
          prepare_ajax();          
          loadKeywords();
          update_messenger();
      },
      error: function(answer) {
        console.log(answer.responseText);
        update_messenger();
      },
    });  
  });

  $('#add_character').off();
  $('#add_character').on('click',function(event){
    event.preventDefault();
    $.ajax({
      url: 'ajax/add/character/',
      success: function(answer) {
        $('.details').html('done')
          rebootlinks();
          prepare_ajax();          
          loadKeywords();
          update_messenger();
      },
      error: function(answer) {
        $('.details').html('oops, broken')
        rebootlinks();
        update_messenger();
      },

    });
  });

  $('#conf_details').off();
  $('#conf_details').on('click',function(event){
    event.preventDefault();
    $.ajax({
      url: 'ajax/conf_details/',
      success: function(answer) {
        console.log(answer);
        $('.details').html(answer)
        rebootlinks();
        update_messenger();
      },
    });
  });

  $('#build_config_pdf').off();
  $('#build_config_pdf').on('click',function(event){
    event.preventDefault();
    $.ajax({
      url: 'ajax/build_config_pdf/',
    }).done(function(answer) {
        console.log(answer.comment);
        $('.details').html(answer.comment);
        rebootlinks();
        update_messenger();
    });
  });


  $('#build_pdf_rules').off();
  $('#build_pdf_rules').on('click',function(event){
    event.preventDefault();
    $.ajax({
      url: 'ajax/build_pdf_rules/',
    }).done(function(answer) {
        console.log(answer.comment);
        $('.details').html(answer.comment);
        rebootlinks();
        update_messenger();
    });
  });

  $('#seek').off();
  $('#seek').on('click',function(event){
    event.preventDefault();
    key = $('#customize').val(); 
    $.ajax({
      url: 'ajax/view/by_rid/'+key+'/',
      success: function(answer) {
        $('.details').html(answer);
        prepare_ajax();
        rebootlinks();
        update_messenger();
      },
    });
  });



  $('#search').off();
  $('#search').on('click',function(event){
    event.preventDefault();
    event.stopPropagation();
    key = $('#customize').val(); 
    if (key == ''){
      key='none';
    }
    $.ajax({
      url: 'ajax/list/'+key+'/1/',
      success: function(answer) {
        $('.charlist').html(answer);
        prepare_ajax();
        rebootlinks();
        update_messenger();   
      },
    });
  });

  $('.custom_glance').off();
  $('.custom_glance').on('click',function(event){
    event.preventDefault();
    event.stopPropagation();
    $('#customize').val($(this).attr('id'));
    $('#search').click();
  });

  $('.recalc_character').off();
  $('.recalc_character').on('click',function(event){
    event.preventDefault();
    event.stopPropagation();
    var dad = $(this).parents('li').find('div.avatar_link');
    $('li').find('div.avatar_link').removeClass('selected');
    $(dad).addClass('selected');
    $.ajax({      
      url: 'ajax/recalc/character/'+$(this).attr('id')+'/',
      success: function(answer) {
        $('.details').html(answer.character);
        $('li#'+answer.rid).html(answer.link);
        $('li').find('div.avatar_link').removeClass('selected');
        rebootlinks();
        update_messenger();
      },
      error: function(answer){
        console.log('Recalc error...'+answer);
      }
    });
  });

  $('.recalc_pa_character').off();
  $('.recalc_pa_character').on('click',function(event){
    event.preventDefault();
    event.stopPropagation();
    var dad = $(this).parents('li').find('div.avatar_link');
    $('li').find('div.avatar_link').removeClass('selected');
    $(dad).addClass('selected');
    $.ajax({      
      url: 'ajax/recalc_pa/character/'+$(this).attr('id')+'/',
      success: function(answer) {
        $('.details').html(answer.character);
        $('li#'+answer.rid).html(answer.link);
        $('li').find('div.avatar_link').removeClass('selected');
        rebootlinks();
        update_messenger();
      },
      error: function(answer){
        console.log('Recalc error...'+answer);
      }
    });
  });

  $('.recalc_skills_character').off();
  $('.recalc_skills_character').on('click',function(event){
    event.preventDefault();
    event.stopPropagation();
    var dad = $(this).parents('li').find('div.avatar_link');
    $('li').find('div.avatar_link').removeClass('selected');
    $(dad).addClass('selected');
    $.ajax({      
      url: 'ajax/recalc_skills/character/'+$(this).attr('id')+'/',
      success: function(answer) {
        $('.details').html(answer.character);
        $('li#'+answer.rid).html(answer.link);
        $('li').find('div.avatar_link').removeClass('selected');
        rebootlinks();
        update_messenger();
      },
      error: function(answer){
        console.log('Recalc error...'+answer);
      }
    });
  });  

  $('.view_character').off();
  $('.view_character').on('click',function(event){
    console.log('View: '+$(this).attr('id'));
    event.preventDefault();
    event.stopPropagation();
    var dad = $(this).parents('li');
    $('li').removeClass('selected');
    $(dad).addClass('selected');
    $.ajax({      
      url: 'characters/'+$(this).attr('id')+'/view/',
      success: function(answer) {
        $('.details').html(answer)
        $('li').removeClass('selected');        
          rebootlinks();
          prepare_ajax();          
          loadKeywords();
          update_messenger();
      },
      error: function(answer){
        console.log('Vew error...'+answer);
      }
    });
  });

  // Touching skills
  $('th.edit span.fa').off();
  $('th.edit span.fa').on('click',function(event){    
    block = $(this).parent();
    sender = block.attr('id').split('_')[1];
    target = 'val_'+block.attr('id').split('_')[1];
    fingerval = 0;
    if ($(this).hasClass('fa-plus-circle')){
      fingerval = 1;
    }
    if ($(this).hasClass('fa-minus-circle')){
      fingerval = -1;
    }
    console.log(sender);
    console.log(target);
    $.ajax({
      url: 'ajax/skill_touch/',
      method: 'POST',
      headers: {
        'Accept': 'application/json',
        'Content-Type': 'application/x-www-form-urlencoded'
      },
      dataType:'json',
      data: {skill:sender,finger:fingerval},      
      success: function(answer) {
          console.log(answer);
          $('th#'+target).html(answer);
        },
      error: function(answer){
          console.log(answer);
          $('th#'+target).html(answer.responseText);
       },
    });
  
  });

  register_story('epic');
  register_story('drama');
  register_story('act');
  register_story('event');

  $('.tabber').off();
  $('.tabber').on('click', function(event){
    var x = $(this).attr('id');
    $('.tabs').removeClass('tab_up');
    var target = '.tabs#'+x+'t';
    $(target).toggleClass('tab_up');
    console.log(target);
  });

  $('#floatingk').off().on('click', function(event){
    event.preventDefault();
    event.stopPropagation();
    $("ul#keywords").toggleClass("shown");
  });

}

rebootlinks();
