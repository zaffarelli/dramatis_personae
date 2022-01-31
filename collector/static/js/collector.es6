/*
     ╔╦╗╔═╗  ╔═╗┌─┐┬  ┬  ┌─┐┌─┐┌┬┐┌─┐┬─┐
      ║║╠═╝  ║  │ ││  │  ├┤ │   │ │ │├┬┘
     ═╩╝╩    ╚═╝└─┘┴─┘┴─┘└─┘└─┘ ┴ └─┘┴└─
*/
class Collector {
    constructor(ac, op, sc) {
        let me = this;
        me.d3 = undefined;
        me.heartbeat = 0;
        me.ac = ac
        me.op = op
        me.sc = sc
        me.init();
    }

    init() {
        let me = this;
        me.loadKeywords();
    }

    perform() {
        let me = this;
        _.defer(function () {
            me.prepareAjax();
            me.rebootLinks();
        });
    }

    prepareAjax() {
        let me = this;
        $.ajaxSetup({
            beforeSend: function (xhr, settings) {
                if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
                    let csrf_middlewaretoken = $('input[name=csrfmiddlewaretoken]').val();
                    //console.log(csrf_middlewaretoken)
                    xhr.setRequestHeader('X-CSRFToken', csrf_middlewaretoken);
                }
            }
        });
    }

    runHeartbeat(x = 2500) {
        let me = this;
        clearTimeout(me.heartbeat);
        $.ajax({
            url: 'api/heartbeat/',
            success: function (answer) {
                $('#messenger_block').html(answer)
                me.heartbeat = setTimeout("co.runHeartbeat()", x);
            },
        });
    }

    loadKeywords() {
        let me = this;
        $.ajax({
            url: 'api/keywords/',
            success: function (answer) {
                $('#keywords').html('')
                $('#keywords').append(answer.chart);
                me.rebootLinks();
            }
        });
    }

    setToggler(tag, klass, item) {
        let me = this;
        $(tag).off().on('click', function (event) {
            $(item).toggleClass(klass);
            me.rebootLinks();
        });
    }

    shootList(tag, key, page = 1) {
        let me = this;
        $.ajax({
            url: 'ajax/list/' + key + '/' + page + '/',
            success: function (answer) {
                $('.mosaic').html(answer);
                me.prepareAjax();
                me.rebootLinks();
            },
            error: function (answer) {
                console.error('Error getting list for tag=' + tag + ' / key=' + key + ' / page=' + page);
                me.rebootLinks();
            }
        });
    }

    // Auto registering by class
    registerMenuItems() {
        let me = this;
        /* Change all menu-items to ajax/<id> */
        $(".menu-item").off().on("click", function (e) {
            e.preventDefault();
            e.stopPropagation();
            let action_tag = $(this).attr("action");
            let mode_tag = $(this).attr("mode");
            let new_tag = action_tag.replaceAll("_", "/").replaceAll("-PDF", ".pdf")
            let url = 'ajax/' + action_tag + '/';
            if (mode_tag == 'direct') {
                url = new_tag;
                let w = window.open(url, '_blank');
                w.focus();
            }
            console.debug("menu-item " + action_tag + " has been clicked..."+url+' '+mode_tag);
            $.ajax({
                url: url,
                success: function (answer) {
                    if (mode_tag == 'overlay') {
                        $("#d3area").css('display', 'block');
                        console.log(action_tag)
                        if (action_tag == 'deck'){
                            console.log("Epic Deck !!");
                            let epicdeck = new EpicDeck(answer.data, '#d3area');
                            epicdeck.perform();
                        }else {
                            let starmap = new Jumpweb(answer.data, '#d3area');
                            starmap.perform();
                        }
                        me.rebootLinks();
                    } else if (mode_tag == 'index') {
                        let w = window.location.href = "/";
                        // w.focus();
                    } else if (mode_tag == 'main') {
                        $('.mosaic').html(answer.html);
                    } else if (action_tag == 'statistics') {
                        let pre = "<div class='fresque'><div class='tile chart_panel'>";
                        let post = "</div></div>";
                        console.log(answer.mosaic);
                        $('.mosaic').html(pre + answer.mosaic + post);
                    } else {
                        $('.mosaic').html(answer.mosaic);
                    }
                    me.rebootLinks();
                    //ac.reset(x, "sheet_" + answer.id, "customizer");
                },
                error: function (answer) {
                    console.error('Error on menu-item [' + action_tag + ']');
                    console.debug(answer)
                    me.rebootLinks();
                }
            });
        });
    }

    registerSlugItems() {
        let me = this;
        /* Change all menu-items to ajax/<id> */
        $(".slug-item").off().on("click", function (e) {
            e.preventDefault();
            e.stopPropagation();
            let action_tag = $(this).attr("action");
            let mode_tag = $(this).attr("mode");
            let slug = $('#customize').val();
            if (slug == '') {
                slug = 'none';
            }
            let x = me.btoasafe(slug)
            console.log('-->' + x + " (" + slug + ")")
            console.debug(action_tag + " has been clicked...");
            $.ajax({
                url: 'ajax/' + action_tag + '/' + x + '/',
                success: function (answer) {
                    if (mode_tag == 'overlay') {
                        $("#d3area").css('display', 'block');
                        let starmap = new OrbitalMap(answer.data, '#d3area');
                        starmap.perform();
                        me.rebootLinks();
                    } else {
                        $('.mosaic').html(answer.mosaic);
                    }
                    me.rebootLinks();
                },
                error: function (answer) {
                    console.error('Error on slug-item [' + action_tag + ']');
                    console.debug(answer)
                    me.rebootLinks();
                }
            });
        });
    }

    btoasafe(str) {
        let enc = btoa(str);
        let safe = enc.replace(/=/g, '_');
        // let safe = enc.replace(/-/g, '+').replace(/_/g, '/')
        // let pad = safe.length % 4;
        // if(pad) {
        //   if(pad === 1) {
        //     throw new Error('InvalidLengthError: Input base64url string is the wrong length to determine padding');
        //   }
        //   safe += new Array(5-pad).join('=');
        // }
        return (safe);
    }

    registerPullDowns() {
        $(".pull-down").off().on("click", function (e) {
            e.preventDefault();
            e.stopPropagation();
            console.log("toggle hidden")
            let dad = $(this).parents("li");
            let sub = $(dad).find("ul.level-2");
            $(sub).toggleClass("off");
        });
    }

    registerFigures() {
        $(".figureshow").off().on("click", function (e) {
            e.preventDefault();
            e.stopPropagation();
            $("#figure").attr("src", $(this).attr("medimg"));
            $("#figurebox").css("display", "block");
        });
        $("#figure").off().on("click", function (e) {
            e.preventDefault();
            e.stopPropagation();
            $("#figurebox").css("display", "none");
        });
    }

    registerCharsels() {
        let me = this;
        $(".charsel").off().on("click", function (e) {
            e.preventDefault();
            e.stopPropagation();
            console.log('Charsel click');
            let key = $(this).attr('ref');
            console.log('key:'+key);
            $.ajax({
                url: 'ajax/deep_toggle/selected/' + key  +'/',
                success: function (answer) {
                    console.log(answer);
                    me.prepareAjax();
                    me.rebootLinks();
                },
                error: function (answer) {
                    console.error(answer);
                    me.rebootLinks();
                }
            });
        });
    }


    registerSlugPageItems() {
        let me = this;
        /* Change all menu-items to ajax/<id> */
        $(".slug-page-item").off().on("click", function (e) {
            e.preventDefault();
            e.stopPropagation();
            let action_tag = $(this).attr("action");
            let page = $(this).attr("page");
            let slug = $('#customize').val().trim();
            let code = $(this).attr('code');
            if (code !== undefined) {
                slug = code;
                $('#customize').val(code);
            }
            if (slug == '') {
                slug = 'none';
            }
            let x = me.btoasafe(slug)
            let aurl = 'ajax/' + action_tag + '/' + x + '/' + page + '/';
            console.debug(action_tag + " has been clicked... (" + aurl + ")");
            $.ajax({
                url: aurl,
                success: function (answer) {
                    $('.mosaic').html(answer.mosaic);
                    me.rebootLinks();
                },
                error: function (answer) {
                    console.error('Error on slug-page-item [' + action_tag + ']');
                    console.debug(answer)
                    me.rebootLinks();
                }
            });
        });
    }

    markButtons() {
        $('.menu-item').addClass('highlighted');
        $('.slug-item').addClass('highlighted');
        $('.slug-page-item').addClass('highlighted');
    }

    rebootLinks() {
        let me = this;
        me.sc.doConnect(me);
        me.op.doConnect(me);
        me.ac.prepareEvents(me);
        /* Starting Heartbeat */
        me.heartbeat = setTimeout("co.runHeartbeat()", 2500);

        /* Automatic ajax pipelining */
        me.registerMenuItems();
        me.registerSlugItems();
        me.registerSlugPageItems();
        me.registerPullDowns();
        me.registerFigures();
        me.registerCharsels();
        /* Togglers */
        me.setToggler('.mobile_form_toggler', 'collapsed', "#customizer");
        me.setToggler('.menu_right_toggler', 'collapsed', ".menuright");
        me.setToggler('.list_toggler', 'collapsed', ".list");
        me.setToggler('#menu_right_toggler', 'collapsed', ".menuright");
        me.setToggler('#listtoggler', 'collapsed', ".list");
        me.setToggler('.dicer_toggler', 'collapsed', ".dicer");
        me.setToggler('#dicer_toggler', 'collapsed', ".dicer");
        //         me.markButtons();
        $('.character_name').off().on('click', function (event) {
            event.preventDefault();
            event.stopPropagation();
            let mine = $(this).parents('div.avatar_link').find('div.character_info');
            $('div.avatar_link').find('div.character_info').addClass('hidden');
            $(mine).toggleClass('hidden');
            me.rebootLinks();
        });

        $('#area_close').off().on('click', function (event) {
            $("#d3area").css('display', 'none');
        })

        $('#board_area_close').off().on('click', function (event) {
            $("#board").css('display', 'none');
            $("#board").html('');
        })

        $('.recalc_avatar').off().on('click', function (event) {
            event.preventDefault();
            event.stopPropagation();
            let dad = $(this).parents('li');
            let x = $(this).parents('div').attr("id").split("_")[1];
            let dad_id = $(dad).attr("id");
            //let that_id = $(this).attr('id').split("_")[0];
            $("li#" + dad_id + " .character_info").removeClass('hidden');
            $.ajax({
                url: 'ajax/recalc/avatar/' + x + '/',
                success: function (answer) {
                    $('#board').html('<div id="the_tile"></div><div id="board_area_close"><i class="golden fa fa-times-circle"></i></div>');
                    // $('.tile').removeClass("sheet_tile");
                    $('#the_tile').addClass("sheet_tile");
                    $('#the_tile').html(answer.character);
                    // $('.character_row').removeClass("sheet_tile");
                    // $('#row_' + x).addClass("sheet_tile");
                    // $('#row_' + x).html(answer.character);
                    $('#board').css('display', 'block');

                    $('li#' + answer.rid).html(answer.link);
                    $('#customizer').html(answer.mobile_form);
                    ac.reset(x, "sheet_" + x, "customizer");
                    $("li#" + dad_id + " .character_name").click();
                    me.rebootLinks();
                    //update_messenger();
                },
                error: function (answer) {
                    console.log('Recalc error...' + answer);
                }
            });
        });
        $('.sheet').off().on('click', function (event) {
            event.preventDefault();
            event.stopPropagation();
            let dad = $(this).parents('li');
            let x = $(this).parents('div').attr("id").split("_")[1];
            let dad_id = $(dad).attr("id");
            if (x == undefined) {
                x = $(this).attr("id").split("_")[1];
            }
            $("li#" + dad_id + " .character_info").removeClass('hidden');
            $.ajax({
                url: 'ajax/sheet/avatar/' + x + '/',
                success: function (answer) {
                    $("#d3area").css('display', 'block');
                    let s = JSON.parse(answer.settings);
                    let d = JSON.parse(answer.data);
                    me.d3 = new FICSSheet(s, "#d3area", me);
                    me.d3.perform(d);
                    me.rebootLinks();
                },
                error: function (answer) {
                    console.error('Sheet display error...' + answer);
                }
            });
        });
        $('.jumpweb').off().on('click', function (event) {
            event.preventDefault();
            event.stopPropagation();
            // console.log('Jumpweb !!!');
            $.ajax({
                url: 'ajax/jumpweb/',
                success: function (answer) {
                    $("#d3area").css('display', 'block');
                    // console.log('Data received !!!');
                    // console.log(answer.data);
                    //let d = JSON.parse(answer.data);
                    let starmap = new Jumpweb(answer.data, '#d3area');
                    starmap.perform();
                    me.rebootLinks();
                },
                error: function (answer) {
                    console.error('Jumpweb display error...');
                    console.error(answer);
                }
            });
        });

        $('.orbital').off().on('click', function (event) {
            event.preventDefault();
            event.stopPropagation();
            $.ajax({
                url: 'ajax/jumpweb/',
                success: function (answer) {
                    $("#d3area").css('display', 'block');
                    console.log(answer)
                    let orbital = new OrbitalMap(answer.data, '#d3area');
                    orbital.perform();
                    me.rebootLinks();
                },
                error: function (answer) {
                    console.error('Orbital Map display error...');
                    console.error(answer);
                }
            });
        });


        $('.edit_character').off()
            .on('click', function (event) {
                event.preventDefault();
                event.stopPropagation();
                let dad = $(this).parents('li');
                let dad_id = $(dad).attr("id");
                let x = $(this).parents('div').attr("id").split("_")[1];
                $("li#" + dad_id + " .character_info").removeClass('hidden');
                $.ajax({
                    url: 'ajax/edit/avatar/' + x + '/',
                    success: function (answer) {
                        $('#board').html('<div id="the_tile"></div><div id="board_area_close"><i class="golden fa fa-times-circle"></i></div><div id="board_area_valid"><i id="menu_go" class="golden fa fa-play-circle"></i></div>');
                        $('#the_tile').addClass("sheet_tile");
                        $('#the_tile').html(answer);
                        $('#board').css('display', 'block');
                        me.rebootLinks();
                        ac.reset(x, "sheet_" + x, "customizer");
                        $("li#" + dad_id + " .character_name").click();
                    },
                    error: function (answer) {
                        console.log('Error on editing ' + x);
                        me.rebootLinks();
                    }
                });
            });

        $("#menu_login").off().on('click',
            function (event) {
                event.preventDefault();
                $.ajax({
                    type: "GET",
                    url: '/ajax/login/',
                    data: $('#login_form').serialize(),
                    success: function (answer) {
                        $('#login_block').html(answer);
                        me.rebootLinks();
                    },
                    error: function (answer) {
                        $('.details').html(answer);
                        me.rebootLinks();
                    }
                });
            }
        );

        $("#login_button").off().on('click',
            function (event) {
                event.preventDefault();
                console.log("Login post !!!")
                $.ajax({
                    type: "POST",
                    url: '/ajax/login/',
                    data: $('#login_form').serialize(),
                    success: function (answer) {
                        $('.user_block').html(answer);
                        window.location = '/';
                    },
                    error: function (answer) {
                        $('.details').html(answer);
                        me.rebootLinks();
                    }
                });
            }
        );

        $("#menu_logout").off().on('click',
            function (event) {
                event.preventDefault();
                $.ajax({
                    type: "POST",
                    url: '/ajax/logout/',
                    success: function (answer) {
                        $('.user_block').html(answer);
                        window.location = '/';
                    },
                    error: function (answer) {
                        $('.user_block').html(answer);
                        me.rebootLinks();
                    }
                });
            }
        );

        $('.wa_export_character').off().on('click',
            function (event) {
                event.preventDefault();
                event.stopPropagation();
                let dad = $(this).parents('li');
                let x = $(this).parents('div').attr("id").split("_")[1];
                let dad_id = $(dad).attr("id");
                $("li#" + dad_id + " .character_info").removeClass('hidden');
                $.ajax({
                    url: 'ajax/wa_export/character/' + x + '/',
                    success: function (answer) {
                        $('.details').html(answer.character);
                        me.rebootLinks();
                    },
                    error: function (answer) {
                        console.log('Recalc error...' + answer);
                    }
                });
            }
        );

        $('.toggle_public').off().on('click',
            function (event) {
                event.preventDefault();
                let dad = $(this).parents('li');
                let x = $(this).parents('div').attr("id").split("_")[1];
                let dad_id = $(dad).attr("id");
                $("li#" + dad_id + " .character_info").removeClass('hidden');
                $("li#" + dad_id + " .avatar_link").css('border-color', 'red');
                $.ajax({
                    url: 'toggle/' + x + '/public',
                    success: function (answer) {
                        console.log(answer)
                        $('li#' + dad_id).html(answer.avatar_link);
                        me.rebootLinks();
                    },
                    error: function (answer) {
                        console.warn('Error on toggle...');
                    },
                });
            }
        );

        $('.toggle_spotlight').off().on('click',
            function (event) {
                event.preventDefault();
                let dad = $(this).parents('li');
                let x = $(this).parents('div').attr("id").split("_")[1];
                let dad_id = $(dad).attr("id");
                $("li#" + dad_id + " .character_info").removeClass('hidden');
                $("li#" + dad_id + " .avatar_link").css('border-color', 'red');
                console.log(x);
                $.ajax({
                    url: 'toggle/' + x + '/spotlight',
                    success: function (answer) {
                        console.log(answer)
                        $('li#' + dad_id).html(answer.avatar_link);
                        me.rebootLinks();
                    },
                    error: function (answer) {
                        console.warn('Error on toggle...');
                    },
                });
            }
        );

        $("#menu_recalc").off().on('click',
            function (event) {
                event.preventDefault();
                event.stopPropagation();
                $.ajax({
                    url: 'api/recalc/',
                    success: function (answer) {
                        me.runHeartbeat();
                        me.rebootLinks();
                    },
                    error: function (answer) {
                        console.error("Ooops");
                        console.log(answer);
                        me.runHeartbeat();
                        me.rebootLinks();
                    }
                });
            });

        $('#menu_todo').off().on('click',
            function (event) {
                event.preventDefault();
                event.stopPropagation();
                $.ajax({
                    url: 'todo/show',
                    success: function (answer) {
                        //$('.charlist').html(answer)
                        $('.mosaic').html(answer)
                        me.prepareAjax();
                        me.rebootLinks();
                    },
                    error: function (answer) {
                        console.error('ooops... on show jumpweb...');
                    }
                });
            });

        $('#menu_go').off().on('click',
            function (event) {
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
                    success: function (answer) {
                        $('#tile_back_' + id).click();
                        me.rebootLinks();
                        me.prepareAjax();
                        me.loadKeywords();
                    },
                    error: function (answer) {
                        console.log(answer.responseText);
                    },
                });
            });

        $('.tile_back').off().on('click',
            function (event) {
                event.preventDefault();
                let full_id = $(this).attr('id');
                let id = full_id.split("_")[2];
                $('.tile').removeClass('sheet_tile');

                $.ajax({
                    url: 'ajax/tile/avatar/' + id + '/',
                    success: function (answer) {
                        $('#tile_' + id).html(answer);
                        me.rebootLinks();
                    },
                    error: function (answer) {
                        console.error(answer);
                        me.rebootLinks();
                    },
                });
            });

        /* Other links */
        $('.edit_investigator').off().on('click',
            function (event) {
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
                    success: function (answer) {
                        $('.details').html(answer);
                        $('li#' + answer.rid).html(answer.link);
                        me.rebootLinks();
                        ac.reset(x, "sheet_" + x, "customizer");
                        $("li#" + dad_id + " .character_name").click();
                        //update_messenger();
                    },
                    error: function (answer) {
                        console.log('ooops... :(');
                        //update_messenger();
                    }
                });
            });
        $('.roll_dice').off().on('keypress',
            function (event) {
                if (event.which == 13) {
                    event.preventDefault();
                    event.stopPropagation();
                    console.log("enter key pressed")
                    let formula = $(this).val().toLowerCase().replace(" ", "_").replace("+", "x").replace("!", "i")
                    console.log(formula)
                    $.ajax({
                        url: 'ajax/roll_dice/' + formula + '/',
                        success: function (answer) {
                            $('.rolls').html(answer.rolls);
                            $('.mods').html(answer.mods);
                            $('.total').html(answer.total);
                            me.rebootLinks();
                            //pdate_messenger();
                        },
                        error: function (answer) {
                            console.log('Broken dice... :(');
                            //update_messenger();
                        }
                    });
                }
            });
        $('.dice_roll').off().on('click',
            function (event) {
                event.preventDefault();
                event.stopPropagation();
                let arr = $(this).attr("id").split("-")
                console.log(arr)
                $("#set").val("1d12+" + arr[1]);
                //$("#throw").fireEvent('mouseup');
                $t.raise_event($t.id('throw'), 'mouseup');
                me.rebootLinks();
            });
    }
}