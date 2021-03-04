/*
     ╔╦╗╔═╗  ╔═╗┌─┐┬  ┬  ┌─┐┌─┐┌┬┐┌─┐┬─┐
      ║║╠═╝  ║  │ ││  │  ├┤ │   │ │ │├┬┘
     ═╩╝╩    ╚═╝└─┘┴─┘┴─┘└─┘└─┘ ┴ └─┘┴└─
*/

class Collector{
    constructor(ac,op,sc){
        let me = this;
        me.heartbeat = 0;
        me.ac = ac
        me.op = op
        me.sc = sc
        me.init();
    }

    init(){
        let me = this;
        _.defer(function(){
            me.rebootLinks();
            me.prepareAjax();
            me.loadAjax();
            me.loadKeywords();
        });
    }

    loadAjax() {
        let me = this;
        $.ajax({
            url: 'ajax/storyline/none/',
            success: function(answer) {
                $('.storyline').html(answer)
                $.ajax({
                    url: 'ajax/list/none/1/',
                    success: function(answer) {
                        $('.mosaic').html(answer)
                        me.rebootLinks();
                    },
                });
            },
        });
        me.setToggler('.mobile_form_toggler', 'collapsed', "#customizer");
        me.setToggler('.menu_right_toggler', 'collapsed', ".menuright");
        me.setToggler('.list_toggler', 'collapsed', ".list");
        me.setToggler('#menu_right_toggler', 'collapsed', ".menuright");
        me.setToggler('#listtoggler', 'collapsed', ".list");
        me.setToggler('.dicer_toggler', 'collapsed', ".dicer");
        me.setToggler('#dicer_toggler', 'collapsed', ".dicer");
    }

    prepareAjax() {
        let me = this;
        $.ajaxSetup({
            beforeSend: function(xhr, settings) {
                if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
                    let csrf_middlewaretoken = $('input[name=csrfmiddlewaretoken]').val();
                    //console.log(csrf_middlewaretoken)
                    xhr.setRequestHeader('X-CSRFToken', csrf_middlewaretoken);
                }
            }
        });
    }

    runHeartbeat(x=5000){
        let me = this;
        clearTimeout(me.heartbeat);
        $.ajax({
            url: 'api/heartbeat/',
            success: function(answer) {
                $('#messenger_block').html(answer)
                me.heartbeat = setTimeout("co.runHeartbeat()", x);
            },
        });
    }

    keywordHandlerClick(event) {
        let me = this;
        let firstPoint = chart_keywords.getElementAtEvent(event)[0];
        if (firstPoint) {
            let label = chart_keywords.data.labels[firstPoint._index];
            let value = chart_keywords.data.datasets[firstPoint._datasetIndex].data[firstPoint._index];
            $('#customize').val(label);
            $('#menu_search').click();
        }
    }

    loadKeywords() {
        let me = this;
        $.ajax({
            url: 'api/keywords/',
            success: function(answer) {
                $('#keywords').html('')
                $('#keywords').append(answer.chart);
                me.rebootLinks();
            }
        });
    }

    setToggler(tag, klass, item) {
        let me = this;
        $(tag).off().on('click', function(event) {
            $(item).toggleClass(klass);
            me.rebootLinks();
        });
    }

    shootList(tag,key,page=1){
        let me = this;
        $.ajax({
            url: 'ajax/list/' + key + '/' + page + '/',
            success: function(answer) {
                $('.mosaic').html(answer)
                me.prepareAjax();
                me.rebootLinks();
            },
            error: function(answer) {
                console.error('Error getting list for tag='+tag+' / key='+key+' / page='+page);
                me.rebootLinks();
            }
        });
    }



    rebootLinks() {
        let me = this;
        me.sc.doConnect(me);
        me.op.doConnect(me);
        me.ac.prepareEvents(me);


        me.heartbeat = setTimeout("co.runHeartbeat()", 500);

        /* List based actions (Those rebuild the list everytime) */

        $('.nav').off().on('click', function(event) {
            event.preventDefault();
            event.stopPropagation();
            let tag = "nav";
            let key = $('#customize').val();
            let page = $(this).attr('page');
            if (key == '') {
                key = 'none';
            }
            me.shootList(tag,key,page);
        });
        $('.episode_cast').off().on('click', function(event) {
            event.preventDefault();
            event.stopPropagation();
            let tag = "episode_cast";
            let key = $(this).attr('id');
            let page = $(this).attr('page');
            $('#customize').val(key);
            me.shootList(tag,key,page);
        });
        $("#menu_search").off().on('click', function(event) {
            event.preventDefault();
            event.stopPropagation();
            let tag = "menu_search";
            let key = $('#customize').val();
            let page = $(this).attr('page');
            if (key == '') {
                key = 'none';
            }
            me.shootList(tag,key,page);
        });

//        $("#menu_seek").off().on('click', function(event) {
//            event.preventDefault();
//            event.stopPropagation();
//            let tag = "RID seek";
//            let key = $('#customize').val();
//            if (key == '') {
//                key = 'none';
//            }
//            let page = $(this).attr('page');
//            me.shootList(tag,key,page);
////            $.ajax({
////                url: 'ajax/view/by_rid/' + key + '/',
////                success: function(answer) {
////                    $('.details').html(answer.character);
////                    $('.avatars').html("");
////                    _.forEach(answer.links,function(e){
////                        $('.avatars').append("<li id='"+e.rid + "'>" + e.data + "</li>");
////                    })
////                    me.prepareAjax();
////                    me.rebootLinks();
////                },
////                error: function(answer) {
////                    console.error('Seek error...');
////                    console.error(answer.character);
////                }
////            });
//        });

        $('.custom_glance').off().on('click', function(event) {
            event.preventDefault();
            event.stopPropagation();
            $('#customize').val($(this).attr('id'));
            $('#search').click();
        });
//        $('.character_link').off().on('click', function(event) {
//            event.preventDefault();
//            event.stopPropagation();
//            $.ajax({
//                url: 'ajax/recalc/character/' + $(this).attr('id') + '/',
//                success: function(answer) {
//                    $('.details').html(answer.character);
//                    me.rebootLinks();
//                    ac.reset(answer.id, "sheet_" + answer.id, "customizer");
//                },
//                error: function(answer) {
//                    console.log('Recalc error...' + answer);
//                }
//            });
//        });
        $('.character_name').off().on('click', function(event) {
            event.preventDefault();
            event.stopPropagation();
            let mine = $(this).parents('div.avatar_link').find('div.character_info');
            $('div.avatar_link').find('div.character_info').addClass('hidden');
            $(mine).toggleClass('hidden');
            me.rebootLinks();
        });
        $('.recalc_avatar').off().on('click', function(event) {
            event.preventDefault();
            event.stopPropagation();
            let dad = $(this).parents('li');
            let x = $(this).parents('div').attr("id").split("_")[1];
            let dad_id = $(dad).attr("id");
            //let that_id = $(this).attr('id').split("_")[0];
            $("li#" + dad_id + " .character_info").removeClass('hidden');
            $.ajax({
                url: 'ajax/recalc/avatar/' + x + '/',
                success: function(answer) {
                    $('.tile').removeClass("sheet_tile");
                    $('#tile_'+x).addClass("sheet_tile");
                    $('#tile_'+x).html(answer.character);
                    $('li#' + answer.rid).html(answer.link);
                    $('#customizer').html(answer.mobile_form);
                    ac.reset(x, "sheet_" + x, "customizer");
                    $("li#" + dad_id + " .character_name").click();
                    me.rebootLinks();
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
//            console.log(x);
            //let that_id = $(this).attr('id').split("_")[0];
            $("li#" + dad_id + " .character_info").removeClass('hidden');
            $.ajax({
                url: 'ajax/edit/avatar/' + x + '/',
                success: function(answer) {
                    $('.tile').removeClass("sheet_tile");
                    $('#tile_'+x).addClass("sheet_tile");
                    $('#tile_'+x).html(answer);
                    $('li#' + answer.rid).html(answer.link);
                    me.rebootLinks();
                    ac.reset(x, "sheet_" + x, "customizer");
                    $("li#" + dad_id + " .character_name").click();
                    //update_messenger();
                },
                error: function(answer) {
                    console.log('Error on editing '+x);
                    me.rebootLinks();
                    //update_messenger();
                }
            });
        });

        $("#menu_conf_details").off().on('click', function(event) {
            event.preventDefault();
            $.ajax({
                url: 'ajax/conf_details/',
                success: function(answer) {
                    $('.mosaic').html(answer)
                    me.rebootLinks();
                },
            });
        });
        $("#menu_build_config_pdf").off().on('click', function(event) {
            event.preventDefault();
            $.ajax({
                url: 'ajax/build_config_pdf/',
            }).done(function(answer) {
                $('.details').html(answer.comment);
                me.rebootLinks();
            });
        });
        $("#menu_login").off().on('click', function(event) {
            event.preventDefault();
            $.ajax({
                type:"GET",
                url: '/ajax/login/',
                data: $('#login_form').serialize(),
                success: function(answer){
                    $('#login_block').html(answer);
                    me.rebootLinks();
                },
                error: function(answer) {
                    $('.details').html(answer);
                    me.rebootLinks();
                }
            });
        });
        $("#login_button").off().on('click', function(event) {
            event.preventDefault();
            console.log("Login post !!!")
            $.ajax({
                type:"POST",
                url: '/ajax/login/',
                data: $('#login_form').serialize(),
                success: function(answer){
                    $('.user_block').html(answer);
                    window.location = '/';
                },
                error: function(answer) {
                    $('.details').html(answer);
                    me.rebootLinks();
                }
            });
        });
        $("#menu_logout").off().on('click', function(event) {
            event.preventDefault();
            $.ajax({
                type:"POST",
                url: '/ajax/logout/',
                success: function(answer){
                    $('.user_block').html(answer);
                    window.location = '/';
                },
                error: function(answer) {
                    $('.user_block').html(answer);
                    me.rebootLinks();
                }
            });
        });

        $("#menu_profile").off().on('click', function(event) {
            event.preventDefault();
            $.ajax({
                type:"POST",
                url: '/ajax/profile/',
                success: function(answer){
                    $('.details').html(answer);
                    console.log('profile ok')
                    me.rebootLinks();
                },
                error: function(answer) {
                    console.log('Error!!!')
                    $('.details').html(answer);
                    me.rebootLinks();
                }
            });
        });

        $('.wa_export_character').off().on('click', function(event) {
            event.preventDefault();
            event.stopPropagation();
            let dad = $(this).parents('li');
            let x = $(this).parents('div').attr("id").split("_")[1];
            let dad_id = $(dad).attr("id");
            //let that_id = $(this).attr('id').split("_")[0];
            $("li#" + dad_id + " .character_info").removeClass('hidden');
            $.ajax({
                url: 'ajax/wa_export/character/' + x + '/',
                success: function(answer) {
                    $('.details').html(answer.character);
                    me.rebootLinks();

                },
                error: function(answer) {
                    console.log('Recalc error...' + answer);
                }
            });
        });


        $('#menu_build_pdf_rules').off().on('click', function(event) {
            event.preventDefault();
            $.ajax({
                url: 'ajax/build_pdf_rules/',
            }).done(function(answer) {
                //$('.details').html(answer);
                me.rebootLinks();
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
                    me.rebootLinks();
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
                    me.rebootLinks();
                },
                error: function(answer) {
                    console.warn('Error on toggle...');
                },
            });
        });
        $('#current_storyline').off('change').on('change', function(event) {
            event.preventDefault();
            event.stopPropagation();
            let slug = $('#current_storyline').val();
            console.log(slug);
            $.ajax({
                url: 'ajax/storyline/' + slug + '/',
                success: function(answer) {
                    $('.storyline').html(answer)
                    $.ajax({
                        url: 'ajax/list/none/1/',
                        success: function(answer) {
                            //$('.charlist').html(answer)

                            $('.mosaic').html(answer)
                            //me.rebootLinks();
                            window.location = '/';
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
                    $('.mosaic').html('')
                    answer.charts.forEach(function(elem) {
                        $('.mosaic').append(elem);
                    });
                    me.rebootLinks();
                },
            });
            me.rebootLinks();
        });
        $("#menu_recalc").off().on('click', function(event) {
            event.preventDefault();
            event.stopPropagation();
            $.ajax({
                url: 'api/recalc/',
                success: function(answer) {
                    me.runHeartbeat();
                    me.rebootLinks();
                },
                error: function(answer){
                    console.error("Ooops");
                    console.log(answer);
                    me.runHeartbeat();
                    me.rebootLinks();
                }
            });
        });
//         $('#menu_jumpweb').off().on('click', function(event) {
//             event.preventDefault();
//             event.stopPropagation();
//             $.ajax({
//                 url: 'show_jumpweb  ',
//                 success: function(answer) {
//                     $('.details').html(answer);
//                     let tab = window.open(null,'graphics');
//                     tab.document.write(answer)
//
//                     me.prepareAjax();
//                     me.rebootLinks();
// //                    let html = "<!DOCTYPE html><html>yo</html>";
// //                    //let spacecharts = window.open("data:text/html," + encodeURIComponent(html),"Spacecharts");
// //                    let spacecharts = window.open("about:blank","spacecharts");
// //                    spacecharts.focus();
//                 },
//                 error: function(answer) {
//                     console.error('ooops... on show jumpweb...');
//                 }
//             });
//         });
        $('#menu_todo').off().on('click', function(event) {
            event.preventDefault();
            event.stopPropagation();
            $.ajax({
                url: 'todo/show',
                success: function(answer) {
                    //$('.charlist').html(answer)
                    $('.mosaic').html(answer)
                    me.prepareAjax();
                    me.rebootLinks();
                },
                error: function(answer) {
                    console.error('ooops... on show jumpweb...');
                }
            });
        });
        $('#menu_go').off().on('click', function(event) {
            event.preventDefault();
            event.stopPropagation();

            let formdata = $('.character_form').serialize();
            let id = $('.character_form input[name=id]').val();
            let rid = $('.character_form input[name=rid]').val();

            let tgt = $('.character_form').attr('form-target');

            $.ajax({
                url: 'ajax/edit/avatar/' + id + '/',
                type: 'POST',
                headers: {
                    'Accept': 'application/json',
                    'Content-Type': 'application/x-www-form-urlencoded'
                },
                data: formdata,
                dataType: 'json',
                success: function(answer) {
                    //$('li').find('div.avatar_link').removeClass('selected');
                    //$('li').find('div.avatar_link').find('#' + id + '.view_character').click();
                    $('#tile_back_'+id).click();
                    me.rebootLinks();
                    me.prepareAjax();
                    me.loadKeywords();
                },
                error: function(answer) {
                    console.log(answer.responseText);
                },
            });
        });
        $('#menu_add_avatar').off().on('click', function(event) {
            event.preventDefault();
            let name = $("#customize").val();
            $("#customize").val("");
            name = name.split(" ").join("-");
            $.ajax({
                url: 'ajax/add/avatar/' + name + '/',
                success: function(answer) {
                    console.log(answer);
                    me.shootList('add_avatar',answer.rid,1);
                },
                error: function(answer) {
                    console.log(answer);
                    console.log('Error on adding')
                    me.rebootLinks();
                },
            });
        });

        $('.tile_back').off().on('click', function(event) {
            event.preventDefault();
            let full_id = $(this).attr('id');
            let id = full_id.split("_")[2];
            $('.tile').removeClass('sheet_tile');

            $.ajax({
                url: 'ajax/tile/avatar/' + id + '/',
                success: function(answer) {
                    console.log(answer);
                    $('#tile_'+id).html(answer);
                },
                error: function(answer) {
                    console.error(answer);
                },
            });
        });


        /* Other links */
        $('.edit_investigator').off().on('click', function(event) {
            event.preventDefault();
            event.stopPropagation();
            let dad = $(this).parents('li');
            let dad_id = $(dad).attr("id");
            let x = $(this).parents('div').attr("id").split("_")[1];
            console.log(x);
            //let that_id = $(this).attr('id').split("_")[0];
            $("li#" + dad_id + " .character_info").removeClass('hidden');
            $.ajax({
                url: 'investigators/' + x + '/edit/',
                success: function(answer) {
                    $('.details').html(answer);
                    $('li#' + answer.rid).html(answer.link);
                    me.rebootLinks();
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
                        me.rebootLinks();
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
            me.rebootLinks();
        });
    }
}

