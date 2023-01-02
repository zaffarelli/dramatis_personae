class Zapp {
    constructor() {
    }

    registerDialogs() {
        /* Register button behavior and display in the board/dialog
        */
        let me = this;
        if (me.co.debug) {
            console.info(">>> Zapp.registerDialogs()");
        }

        $(".dialog_action").off().on("click", function (e) {
            e.preventDefault();
            e.stopPropagation();
            let id = $(this).attr("id");
            let action_tag = $(this).attr("action");
            let param = $(this).attr("param");
            let option = $(this).attr("option");
            if (me.co.debug) {
                console.log(">>>> .dialog_action registered");
            }
            if (id == 'close') {
                /* just close the dialog */
                $("#board").css("display", "none");
            } else {
                if (id == 'update') {
                    let form = '#' + action_tag + '_form';
                    let formdata = $(form).serialize();
                    let urlupdate = action_tag + 's/' + option + '/edit/';
                    console.log(urlupdate)
                    console.log(formdata)
                    $.ajax({
                        url: urlupdate,
                        method: 'POST',
                        headers: {
                            'Accept': 'application/json',
                            'Content-Type': 'application/x-www-form-urlencoded'
                        },
                        data: formdata,
                        dataType: 'json',
                        success: function (answer) {
                            console.log('Success... ');
                            me.co.rebootLinks();

                        },
                        error: function (answer) {
                            console.log('Error... ');
                            console.log(answer);
                            $('.b').html(answer.responseText);
                            me.co.rebootLinks();
                        }
                    });
                } else if (id == "view") {
                    $.ajax({
                        url: action_tag + 's/' + option + '/view/',
                        success: function (answer) {
                            $('#board').html('<div class="a"></div><div class="b" id="card_form_box"></div><div class="c"></div>');
                            $('#card_form_box').html(answer);
                            $("#board").css('display', 'flex');
                            me.co.rebootLinks();

                        },
                        error: function (answer) {
                            console.error('ooops... on view ' + x + ' :(');
                            me.co.rebootLinks();
                        }
                    });

                } else if (id == "edit") {
                    console.log('Edit... ');
                    let urlupdate = action_tag + 's/' + option + '/edit/';
                    $.ajax({
                        url: urlupdate,
                        success: function (answer) {
                            console.log('Success... ');
                            $('#board').html('<div class="a"></div><div class="b" id="card_form_box"></div><div class="c"></div>');
                            $('#card_form_box').html(answer);
                            $("#board").css('display', 'flex');
                            me.co.rebootLinks();
                        },
                        error: function (answer) {
                            console.log('Error... ');
                            console.log(answer);
                            $('.b').html(answer);
                            me.co.rebootLinks();
                        }
                    });
                }
            }
        });
    }

    doConnect(co) {
        let me = this
        me.co = co;
        me.registerDialogs();

    }

}
