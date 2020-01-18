/*
 ╔╦╗╔═╗  ╔═╗┌─┐┬  ┬  ┌─┐┌─┐┌┬┐┌─┐┬─┐
  ║║╠═╝  ║  │ ││  │  ├┤ │   │ │ │├┬┘
 ═╩╝╩    ╚═╝└─┘┴─┘┴─┘└─┘└─┘ ┴ └─┘┴└─
*/

let messenger_tick = null;

function prepare_ajax(){
    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
                var csrf_middlewaretoken = $('input[name=csrfmiddlewaretoken]').val();
                xhr.setRequestHeader('X-CSRFToken',csrf_middlewaretoken);
            }
        }
    });
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

/* Class toggler */
function set_toggler(tag,klass,item){
    $(tag).off().on('click',function(event){
        $(item).toggleClass(klass);
        rebootlinks();
    });
}



function closeMessenger(){
    console.log("Closing messenger...")
    $("#messenger").addClass("hidden");
}

/* Handling messenger */
function update_messenger(){
    $.ajax({
        url: 'ajax/messenger/',
        success: function(answer) {
            if (answer != ""){
                $('#messenger').removeClass("hidden");
                $('#messenger').html(answer);
                clearTimeout(messenger_tick);
                messenger_tick = setTimeout("closeMessenger()",5000);
            }else{
                console.log("no messages")
            }
        },
    });
}

/* On start... */
function rebootlinks(){
    let ac = new AvatarCustomizer();
    let sc = new Scenarist();
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
    $('.episode_cast').off().on('click',function(event){
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
    $('#current_storyline').off().on('change',function(event){
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
    $('#popstats').off().on('click',function(event){
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
          },
      });
      rebootlinks();
    });
    /* Character Edition & Update*/
    $('.edit_character').off().on('click',function(event){
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
    $('#go').off().on('click',function(event){
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
            },
            error: function(answer) {
                console.log(answer.responseText);
            },
        });
    });
    $('#add_character').off().on('click',function(event){
        event.preventDefault();
        var name = $("#customize").val();
        $("#customize").val("");
        name = name.split(" ").join("-");
        $.ajax({
            url: 'ajax/add/character/'+name+'/',
            success: function(answer) {
                //$('.details').html('done')
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
    $('#conf_details').off().on('click',function(event){
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
    $('#build_config_pdf').off().on('click',function(event){
        event.preventDefault();
        $.ajax({
            url: 'ajax/build_config_pdf/',
        }).done(function(answer) {
            console.log(answer.comment);
            $('.details').html(answer.comment);
            rebootlinks();
        });
    });
    $('#build_pdf_rules').off().on('click',function(event){
        event.preventDefault();
        $.ajax({
            url: 'ajax/build_pdf_rules/',
        }).done(function(answer) {
            console.log(answer.comment);
            $('.details').html(answer.comment);
            rebootlinks();
        });
    });
    $('#seek').off().on('click',function(event){
        event.preventDefault();
        key = $('#customize').val();
        $.ajax({
            url: 'ajax/view/by_rid/'+key+'/',
            success: function(answer) {
                $('.details').html(answer);
                prepare_ajax();
                rebootlinks();
            },
        });
    });
    $('#search').off().on('click',function(event){
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
            },
        });
    });
    $('.custom_glance').off().on('click',function(event){
        event.preventDefault();
        event.stopPropagation();
        $('#customize').val($(this).attr('id'));
        $('#search').click();
    });
    $('.recalc_character').off().on('click',function(event){
        event.preventDefault();
        event.stopPropagation();
        console.log("TUTU");
        var dad = $(this).parents('li');

        //$('li').find('div.avatar_link').find('div.character_info').click();
        console.log("li#"+dad_id+" div.avatar_link");
        var dad_id = $(dad).attr("id");
        $("li#"+dad_id+" .character_info").removeClass('hidden');
        $.ajax({
            url: 'ajax/recalc/character/'+$(this).attr('id')+'/',
            success: function(answer) {
                $('.details').html(answer.character);
                $('li#'+answer.rid).html(answer.link);

                rebootlinks();
                //console.log(answer);
                ac.reset(answer.id,"sheet_"+answer.id,"customizer");
                $("li#"+dad_id+" .character_name").click();

            },
            error: function(answer){
                console.log('Recalc error...'+answer);
            }
        });
    });
    // $('.recalc_pa_character').off().on('click',function(event){
    //     event.preventDefault();
    //     event.stopPropagation();
    //     var dad = $(this).parents('li').find('div.avatar_link');
    //     $('li').find('div.avatar_link').removeClass('selected');
    //     $(dad).addClass('selected');
    //     $.ajax({
    //         url: 'ajax/recalc_pa/character/'+$(this).attr('id')+'/',
    //         success: function(answer) {
    //             $('.details').html(answer.character);
    //             $('li#'+answer.rid).html(answer.link);
    //             $('li').find('div.avatar_link').removeClass('selected');
    //             rebootlinks();
    //         },
    //         error: function(answer){
    //             console.log('Recalc error...'+answer);
    //         }
    //     });
    // });
    $('.character_name').off().on('click',function(event){
        event.preventDefault();
        event.stopPropagation();
        var mine = $(this).parents('div.avatar_link').find('div.character_info');
        $('div.avatar_link').find('div.character_info').addClass('hidden');
        $(mine).toggleClass('hidden');
        rebootlinks();
    });
    // $('.recalc_skills_character').off().on('click',function(event){
    //     event.preventDefault();
    //     event.stopPropagation();
    //     var dad = $(this).parents('li').find('div.avatar_link');
    //     $('li').find('div.avatar_link').removeClass('selected');
    //     $(dad).addClass('selected');
    //     $.ajax({
    //         url: 'ajax/recalc_skills/character/'+$(this).attr('id')+'/',
    //         success: function(answer) {
    //             $('.details').html(answer.character);
    //             $('li#'+answer.rid).html(answer.link);
    //             $('li').find('div.avatar_link').removeClass('selected');
    //             rebootlinks();
    //             ac.reset($(this).attr('id'),"toto","here")
    //         },
    //         error: function(answer){
    //             console.log('Recalc error...'+answer);
    //         }
    //     });
    // });
    $('.view_character').off().on('click',function(event){
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
            },
            error: function(answer){
                console.log('Vew error...'+answer);
            }
        });
    });
    /*
    // Touching skills
    $('th.edit span.fa').off().on('click',function(event){
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
    */
    // $('.tabber').off().on('click', function(event){
    //     var x = $(this).attr('id');
    //     $('.tabs').removeClass('tab_up');
    //     var target = '.tabs#'+x+'t';
    //     $(target).toggleClass('tab_up');
    //     console.log(target);
    // });

    sc.doConnect();
    set_toggler('.mobile_form_toggler','collapsed',"#customizer");
    set_toggler('.menu_right_toggler','collapsed',".menuright");
    set_toggler('#menu_right_toggler','collapsed',".menuright");
    update_messenger();
}

/* Startup function for events */
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
/* Here we go! */
rebootlinks();
