/*
 ╔╦╗╔═╗  ╔═╗┌─┐┬  ┬  ┌─┐┌─┐┌┬┐┌─┐┬─┐
  ║║╠═╝  ║  │ ││  │  ├┤ │   │ │ │├┬┘
 ═╩╝╩    ╚═╝└─┘┴─┘┴─┘└─┘└─┘ ┴ └─┘┴└─
*/



let heartbeat = 0;

function prepare_ajax() {
  $.ajaxSetup({
    beforeSend: function(xhr, settings) {
      if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
        var csrf_middlewaretoken = $('input[name=csrfmiddlewaretoken]').val();
        xhr.setRequestHeader('X-CSRFToken', csrf_middlewaretoken);
      }
    }
  });
}

function runHeartbeat(){
    clearTimeout(heartbeat);
    $.ajax({
        url: 'api/heartbeat/',
        success: function(answer) {
            $('#messenger_block').html(answer)
            rebootlinks();
        },
    });
    heartbeat = setTimeout("runHeartbeat()", 1000);
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

function loadKeywords() {
  $.ajax({
    url: 'api/keywords/',
    success: function(answer) {
      $('#keywords').html('')
      $('#keywords').append(answer.chart);
      rebootlinks();
    },
  });
}

/* Class toggler */
function set_toggler(tag, klass, item) {
  $(tag).off().on('click', function(event) {
    $(item).toggleClass(klass);
    rebootlinks();
  });
}


/*
function closeMessenger() {
  console.log("Closing messenger...")
  $("#messenger").addClass("hidden");
}


function update_messenger() {
  $.ajax({
    url: 'ajax/messenger/',
    success: function(answer) {
      if (answer != "") {
        $('#messenger').removeClass("hidden");
        $('#messenger').html(answer);
        clearTimeout(messenger_tick);
        messenger_tick = setTimeout("closeMessenger()", 5000);
      } else {
        console.log("no messages")
      }
    },
  });
}

*/

/* On start... */
function rebootlinks() {
  let ac = new AvatarCustomizer();
  let sc = new Scenarist();
  let op = new Optimizer();
  heartbeat = setTimeout("runHeartbeat()", 1000);
  $('.nav').off();
  $('.nav').on('click', function(event) {
    event.preventDefault();
    event.stopPropagation();
    key = $('#customize').val();
    if (key == '') {
      key = 'none';
    }
    $.ajax({
      url: 'ajax/list/' + key + '/' + $(this).attr('page') + '/',
      success: function(answer) {
        $('.charlist').html(answer)
        rebootlinks();
      },
    });
  });
  $('.episode_cast').off().on('click', function(event) {
    event.preventDefault();
    event.stopPropagation();
    slug = $(this).attr('id');
    $('#customize').val(slug);
    $.ajax({
      url: 'ajax/list/' + slug + '/' + $(this).attr('page') + '/',
      success: function(answer) {
        $('.charlist').html(answer)
        rebootlinks();
      },
    });
  });
  $('#current_storyline').off().on('change', function(event) {
    event.preventDefault();
    event.stopPropagation();
    slug = $('#current_storyline').val();
    console.log(slug);
    $.ajax({
      url: 'ajax/storyline/' + slug + '/',
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
  $('#popstats').off().on('click', function(event) {
    event.preventDefault();
    event.stopPropagation();
    $.ajax({
      url: 'api/popstats/',
      success: function(answer) {
        //console.log(answer.chart1);
        $('.details').html('')
        answer.charts.forEach(function(elem) {
          $('.details').append(elem);
        });
        rebootlinks();
      },
    });
    rebootlinks();
  });

  $('#jumpweb').off().on('click', function(event) {
    event.preventDefault();
    event.stopPropagation();
    $.ajax({
      url: 'jumpweb/show',
      success: function(answer) {

        console.log(answer);
        $('.details').html(answer);
        prepare_ajax();
        rebootlinks();
      },
      error: function(answer) {
        console.error('ooops... on show jumpweb...');
      }
    });
  });

  $('#todo').off().on('click', function(event) {
    event.preventDefault();
    event.stopPropagation();
    $.ajax({
      url: 'todo/show',
      success: function(answer) {
        $('.charlist').html(answer)
        prepare_ajax();
        rebootlinks();
      },
      error: function(answer) {
        console.error('ooops... on show jumpweb...');
      }
    });
  });


  /* Character Edition & Update*/

  $('#go').off().on('click', function(event) {
    event.preventDefault();
    event.stopPropagation();
    var formdata = $('.character_form').serialize();
    var id = $('.character_form input[name=id]').val();
    var rid = $('.character_form input[name=rid]').val();
    $.ajax({
      url: 'characters/' + id + '/edit/',
      method: 'POST',
      headers: {
        'Accept': 'application/json',
        'Content-Type': 'application/x-www-form-urlencoded'
      },
      data: formdata,
      dataType: 'json',
      success: function(answer) {
        $('li').find('div.avatar_link').removeClass('selected');
        $('li').find('div.avatar_link').find('#' + id + '.view_character').click();
        rebootlinks();
        prepare_ajax();
        loadKeywords();
      },
      error: function(answer) {
        console.log(answer.responseText);
      },
    });
  });
  $('#add_character').off().on('click', function(event) {
    event.preventDefault();
    var name = $("#customize").val();
    $("#customize").val("");
    name = name.split(" ").join("-");
    $.ajax({
      url: 'ajax/add/character/' + name + '/',
      success: function(answer) {
        $('.details').html(answer.character)
        rebootlinks();
        prepare_ajax();
        loadKeywords();
      },
      error: function(answer) {
        $('.details').html('oops, broken')
        rebootlinks();
      },
    });
  });

  $('.toggle_public').off().on('click', function(event) {
    event.preventDefault();
    let dad = $(this).parents('li');
    let x = $(this).parents('div').attr("id").split("_")[1];
    let dad_id = $(dad).attr("id");
    $("li#" + dad_id + " .character_info").removeClass('hidden');
    $("li#" + dad_id + " .avatar_link").css('border-color', 'red');
    $.ajax({
      url: 'toggle/' + x + '/public',
      success: function(answer) {
        console.log(answer)
        $('li#' + dad_id).html(answer.avatar_link);
        rebootlinks();
      },
      error: function(answer) {
        console.warn('Error on toggle...');
      },
    });
  });

  $('.toggle_spotlight').off().on('click', function(event) {
    event.preventDefault();
    let dad = $(this).parents('li');
    let x = $(this).parents('div').attr("id").split("_")[1];
    let dad_id = $(dad).attr("id");
    $("li#" + dad_id + " .character_info").removeClass('hidden');
    $("li#" + dad_id + " .avatar_link").css('border-color', 'red');
    console.log(x);
    $.ajax({
      url: 'toggle/' + x + '/spotlight',
      success: function(answer) {
        console.log(answer)
        $('li#' + dad_id).html(answer.avatar_link);
        rebootlinks();
      },
      error: function(answer) {
        console.warn('Error on toggle...');
      },
    });
  });

  $('#conf_details').off().on('click', function(event) {
    event.preventDefault();
    $.ajax({
      url: 'ajax/conf_details/',
      success: function(answer) {
        console.log(answer);
        $('.details').html(answer)
        rebootlinks();
      },
    });
  });
  $('#build_config_pdf').off().on('click', function(event) {
    event.preventDefault();
    $.ajax({
      url: 'ajax/build_config_pdf/',
    }).done(function(answer) {
      console.log(answer.comment);
      $('.details').html(answer.comment);
      rebootlinks();
    });
  });
  $('#build_pdf_rules').off().on('click', function(event) {
    event.preventDefault();
    $.ajax({
      url: 'ajax/build_pdf_rules/',
    }).done(function(answer) {
      console.log(answer.comment);
      $('.details').html(answer.comment);
      rebootlinks();
    });
  });
  // $('#seek').off().on('click', function(event) {
  //   event.preventDefault();
  //   key = $('#customize').val();
  //   $.ajax({
  //     url: 'ajax/view/by_rid/' + key + '/',
  //     success: function(answer) {
  //       $('.details').html(answer);
  //       prepare_ajax();
  //       rebootlinks();
  //     },
  //   });
  // });

  $('#seek').off().on('click', function(event) {
    event.preventDefault();
    event.stopPropagation();
    let key = $('#customize').val();
    //let dad = $(this).parents('li');
    //let dad_id = $(dad).attr("id");
    //$("li#" + dad_id + " .character_info").removeClass('hidden');
    $.ajax({
      url: 'ajax/view/by_rid/' + key + '/',
      success: function(answer) {
        $('.details').html(answer.character);
        $('.avatars').html("");
        _.forEach(answer.links,function(e){
          $('.avatars').append("<li id='"+e.rid + "'>" + e.data + "</li>");
        })

        //$('li#' + answer.rid).html(answer.link);
        prepare_ajax();
        rebootlinks();
        // ac.reset(answer.id, "sheet_" + answer.id, "customizer");
        // $("li#" + dad_id + " .character_name").click();
      },
      error: function(answer) {
        console.log('Seek error...');
        console.log(answer.character);
      }
    });
  });


  $('#search').off().on('click', function(event) {
    event.preventDefault();
    event.stopPropagation();
    key = $('#customize').val();
    if (key == '') {
      key = 'none';
    }
    $.ajax({
      url: 'ajax/list/' + key + '/1/',
      success: function(answer) {
        $('.charlist').html(answer);
        prepare_ajax();
        rebootlinks();
      },
    });
  });
  $('.custom_glance').off().on('click', function(event) {
    event.preventDefault();
    event.stopPropagation();
    $('#customize').val($(this).attr('id'));
    $('#search').click();
  });


  $('.character_link').off().on('click', function(event) {
    event.preventDefault();
    event.stopPropagation();
    $.ajax({
      url: 'ajax/recalc/character/' + $(this).attr('id') + '/',
      success: function(answer) {
        $('.details').html(answer.character);
        rebootlinks();
        ac.reset(answer.id, "sheet_" + answer.id, "customizer");
      },
      error: function(answer) {
        console.log('Recalc error...' + answer);
      }
    });
  });

  $('.character_name').off().on('click', function(event) {
    event.preventDefault();
    event.stopPropagation();
    var mine = $(this).parents('div.avatar_link').find('div.character_info');
    $('div.avatar_link').find('div.character_info').addClass('hidden');
    $(mine).toggleClass('hidden');
    rebootlinks();
  });

  $('.recalc_character').off().on('click', function(event) {
    event.preventDefault();
    event.stopPropagation();
    let dad = $(this).parents('li');
    let x = $(this).parents('div').attr("id").split("_")[1];
    let dad_id = $(dad).attr("id");
    //let that_id = $(this).attr('id').split("_")[0];
    $("li#" + dad_id + " .character_info").removeClass('hidden');
    $.ajax({
      url: 'ajax/recalc/character/' + x + '/',
      success: function(answer) {
        $('.details').html(answer.character);
        $('li#' + answer.rid).html(answer.link);

        $('#customizer').html(answer.mobile_form);
        ac.reset(x, "sheet_" + x, "customizer");
        $("li#" + dad_id + " .character_name").click();
        rebootlinks();
        //update_messenger();
      },
      error: function(answer) {
        console.log('Recalc error...' + answer);
      }
    });
  });

  $('.edit_character').off().on('click', function(event) {
    event.preventDefault();
    event.stopPropagation();
    let dad = $(this).parents('li');
    let dad_id = $(dad).attr("id");
    let x = $(this).parents('div').attr("id").split("_")[1];
    console.log(x);
    //let that_id = $(this).attr('id').split("_")[0];
    $("li#" + dad_id + " .character_info").removeClass('hidden');
    $.ajax({
      url: 'characters/' + x + '/edit/',
      success: function(answer) {
        $('.details').html(answer);
        $('li#' + answer.rid).html(answer.link);
        rebootlinks();
        ac.reset(x, "sheet_" + x, "customizer");
        $("li#" + dad_id + " .character_name").click();
        //update_messenger();
      },
      error: function(answer) {
        console.log('ooops... :(');
        //update_messenger();
      }
    });
  });


  $('.roll_dice').off().on('keypress', function(event) {
    if (event.which == 13){
      event.preventDefault();
      event.stopPropagation();
      console.log("enter key pressed")
      let formula = $(this).val().toLowerCase().replace(" ","_").replace("+","x").replace("!","i")
      console.log(formula)
      $.ajax({
        url: 'ajax/roll_dice/' + formula + '/',
        success: function(answer) {
          $('.rolls').html(answer.rolls);
          $('.mods').html(answer.mods);
          $('.total').html(answer.total);
          rebootlinks();
          //pdate_messenger();
        },
        error: function(answer) {
          console.log('Broken dice... :(');
          //update_messenger();
        }
      });
    }
  });


  // $('.view_character').off().on('click', function(event) {
  //   console.log('View: ' + $(this).attr('id'));
  //   event.preventDefault();
  //   event.stopPropagation();
  //   let dad = $(this).parents('li');
  //   let dad_id = $(dad).attr("id");
  //   let that_id = $(this).attr('id').split("_")[0];
  //   $("li#" + dad_id + " .character_info").removeClass('hidden');
  //   $.ajax({
  //     url: 'characters/' + that_id + '/view/',
  //     success: function(answer) {
  //       $('.details').html(answer)
  //       //$('li#' + answer.rid).html(answer.link);
  //       rebootlinks();
  //       ac.reset(answer.id, "sheet_" + answer.id, "customizer");
  //       $("li#" + dad_id + " .character_name").click();
  //     },
  //     error: function(answer) {
  //       console.log('View error...' + answer);
  //     }
  //   });
  // });

  $('.dice_roll').off().on('click', function(event) {
    event.preventDefault();
    event.stopPropagation();
    let arr = $(this).attr("id").split("-")
    console.log(arr)
    $("#set").val("1d12+"+arr[1]);
    //$("#throw").fireEvent('mouseup');
    $t.raise_event($t.id('throw'), 'mouseup');
    rebootlinks();
  });




  sc.doConnect();
  op.doConnect();
  set_toggler('.mobile_form_toggler', 'collapsed', "#customizer");
  set_toggler('.menu_right_toggler', 'collapsed', ".menuright");
  set_toggler('.list_toggler', 'collapsed', ".list");
  set_toggler('#menu_right_toggler', 'collapsed', ".menuright");
  set_toggler('#list_toggler', 'collapsed', ".list");
  set_toggler('.dicer_toggler', 'collapsed', ".dicer");
  set_toggler('#dicer_toggler', 'collapsed', ".dicer");
//  update_messenger();
}

/* Startup function for events */
function loadajax() {
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
/* Here we go! */
rebootlinks();
