/*
     ╔╦╗╔═╗  ╔═╗┌─┐┬  ┬  ┌─┐┌─┐┌┬┐┌─┐┬─┐
      ║║╠═╝  ║  │ ││  │  ├┤ │   │ │ │├┬┘
     ═╩╝╩    ╚═╝└─┘┴─┘┴─┘└─┘└─┘ ┴ └─┘┴└─
*/

let heartbeat = 0;

function prepareAjax() {
    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
                var csrf_middlewaretoken = $('input[name=csrfmiddlewaretoken]').val();
                xhr.setRequestHeader('X-CSRFToken', csrf_middlewaretoken);
            }
       }
    });
}

function runHeartbeat(x=2500){
    clearTimeout(heartbeat);
    $.ajax({
        url: 'api/heartbeat/',
        success: function(answer) {
            $('#messenger_block').html(answer)
            heartbeat = setTimeout("runHeartbeat()", x);
        },
    });
}



// Chart event handler
function keywordHandlerClick(evt) {
    let firstPoint = chart_keywords.getElementAtEvent(evt)[0];
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
            rebootLinks();
        },
    });
}

function setToggler(tag, klass, item) {
    $(tag).off().on('click', function(event) {
        $(item).toggleClass(klass);
        rebootLinks();
    });
}


function rebootLinks() {
    let ac = new AvatarCustomizer();
    let sc = new Scenarist();
    let op = new Optimizer();
    heartbeat = setTimeout("runHeartbeat()", 2500);

    /* MENU SHORTCUTS */
    $('#menu_current_storyline').off().on('change', function(event) {
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
                        rebootLinks();
                    },
                });
            },
        });
    });

    $("#menu_popstats").off().on('click', function(event) {
        event.preventDefault();
        event.stopPropagation();
        $.ajax({
            url: 'api/popstats/',
            success: function(answer) {
                $('.details').html('')
                answer.charts.forEach(function(elem) {
                    $('.details').append(elem);
                });
                rebootLinks();
            },
        });
        rebootLinks();
    });

    $("#menu_recalc").off().on('click', function(event) {
        event.preventDefault();
        event.stopPropagation();
        $.ajax({
            url: 'api/recalc/',
            success: function(answer) {
                runHeartbeat(2500);
                rebootLinks();
            },
            error: function(answer){
                console.error("Ooops");
                console.log(answer);
            }
        });
        rebootLinks();
    });

    $('#menu_jumpweb').off().on('click', function(event) {
        event.preventDefault();
        event.stopPropagation();
        $.ajax({
            url: 'jumpweb/show',
            success: function(answer) {
                $('.details').html(answer);
                prepareAjax();
                rebootLinks();
            },
            error: function(answer) {
                console.error('ooops... on show jumpweb...');
            }
        });
    });

    $('#menu_todo').off().on('click', function(event) {
        event.preventDefault();
        event.stopPropagation();
        $.ajax({
            url: 'todo/show',
            success: function(answer) {
                $('.charlist').html(answer)
                prepareAjax();
                rebootLinks();
            },
            error: function(answer) {
                console.error('ooops... on show jumpweb...');
            }
        });
    });

    $('#menu_go').off().on('click', function(event) {
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
                rebootLinks();
                prepareAjax();
                loadKeywords();
            },
            error: function(answer) {
                console.log(answer.responseText);
            },
        });
    });

    $('#menu_add_character').off().on('click', function(event) {
        event.preventDefault();
        var name = $("#customize").val();
        $("#customize").val("");
        name = name.split(" ").join("-");
        $.ajax({
            url: 'ajax/add/character/' + name + '/',
            success: function(answer) {
                $('.details').html(answer.character)
                rebootLinks();
                prepareAjax();
                loadKeywords();
            },
            error: function(answer) {
                $('.details').html('oops, broken')
                rebootLinks();
            },
        });
    });


    $("#menu_conf_details").off().on('click', function(event) {
        event.preventDefault();
        $.ajax({
            url: 'ajax/conf_details/',
            success: function(answer) {
                $('.details').html(answer)
                rebootLinks();
            },
        });
    });
  
    $("#menu_build_config_pdf").off().on('click', function(event) {
        event.preventDefault();
        $.ajax({
            url: 'ajax/build_config_pdf/',
        }).done(function(answer) {
            $('.details').html(answer.comment);
            rebootLinks();
        });
    });

    $('#menu_build_pdf_rules').off().on('click', function(event) {
        event.preventDefault();
        $.ajax({
            url: 'ajax/build_pdf_rules/',
        }).done(function(answer) {
            $('.details').html(answer.comment);
            rebootLinks();
        });
    });
  
    $("#menu_seek").off().on('click', function(event) {
        event.preventDefault();
        event.stopPropagation();
        let key = $('#customize').val();
        $.ajax({
            url: 'ajax/view/by_rid/' + key + '/',
            success: function(answer) {
                $('.details').html(answer.character);
                $('.avatars').html("");
                _.forEach(answer.links,function(e){
                    $('.avatars').append("<li id='"+e.rid + "'>" + e.data + "</li>");
                })
                prepareAjax();
                rebootLinks();
            },
            error: function(answer) {
                console.error('Seek error...');
                console.error(answer.character);
            }
        });
    });

    $("#menu_search").off().on('click', function(event) {
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
                prepareAjax();
                rebootLinks();
            },
        });
    });
    
    /* CHARACTER SHORTCUT */
    
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
        rebootLinks();
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
    rebootLinks();
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
        rebootLinks();
        //update_messenger();
      },
      error: function(answer) {
        console.log('Recalc error...' + answer);
      }
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
        rebootLinks();
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
        rebootLinks();
      },
      error: function(answer) {
        console.warn('Error on toggle...');
      },
    });
  });



    /* Other links */

    $('.nav').off().on('click', function(event) {
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
                rebootLinks();
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
                rebootLinks();
            },
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
        rebootLinks();
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
          rebootLinks();
          //pdate_messenger();
        },
        error: function(answer) {
          console.log('Broken dice... :(');
          //update_messenger();
        }
      });
    }
  });


  $('.dice_roll').off().on('click', function(event) {
    event.preventDefault();
    event.stopPropagation();
    let arr = $(this).attr("id").split("-")
    console.log(arr)
    $("#set").val("1d12+"+arr[1]);
    //$("#throw").fireEvent('mouseup');
    $t.raise_event($t.id('throw'), 'mouseup');
    rebootLinks();
  });

  sc.doConnect();
  op.doConnect();
  setToggler('.mobile_form_toggler', 'collapsed', "#customizer");
  setToggler('.menu_right_toggler', 'collapsed', ".menuright");
  setToggler('.list_toggler', 'collapsed', ".list");
  setToggler('#menu_right_toggler', 'collapsed', ".menuright");
  setToggler('#list_toggler', 'collapsed', ".list");
  setToggler('.dicer_toggler', 'collapsed', ".dicer");
  setToggler('#dicer_toggler', 'collapsed', ".dicer");
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
                    rebootLinks();
                },
            });
        },
    });
}

/* Here we go! */
rebootLinks();
