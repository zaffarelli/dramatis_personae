/*
 ╔╦╗╔═╗  ╔═╗┌─┐┬  ┬  ┌─┐┌─┐┌┬┐┌─┐┬─┐
  ║║╠═╝  ║  │ ││  │  ├┤ │   │ │ │├┬┘
 ═╩╝╩    ╚═╝└─┘┴─┘┴─┘└─┘└─┘ ┴ └─┘┴└─
*/
class Scenarist{
    constructor(){
    }

    registerStory(x){
        console.info(">>> Register Story")
        let me = this;
        /* Register all the actions for the scenarist items */
        $('.view_'+x).off().on('click', function(event){
            event.preventDefault();
            event.stopPropagation();
            let t_id = $(this).attr('id')
            let id = t_id.split("_")[t_id.split("_").length-1]
            let children = $(this).parent("p").attr('children');
            let mode_tag = $(this).attr('mode');
            //$(this).css('border-color','red');
            console.log("here we go");
            console.log(x+'s/'+id+'/view/');
            $.ajax({
                url: x+'s/'+id+'/view/',
                success: function(answer) {
                    console.log(mode_tag);
                    if (mode_tag == 'overlay') {
                        $('#board').html('<div class="a"></div><div class="b" id="card_form_box"></div><div class="c"></div>');
                        $('#card_form_box').html(answer);
                        $("#board").css('display','flex');
                        me.co.rebootLinks();
                    }else {
                        $('#' + x + '_' + id).html(answer);

                        me.co.prepareAjax();
                        me.co.rebootLinks();
                        $('#' + x + '_' + id).html(answer);
                        if (children != undefined) {
                            let ch = children.split(";")
                            _.forEach(ch, function (d) {
                                $("#view_" + d).click();
                            })
                        }
                    }
                    me.co.prepareAjax();
                    me.co.rebootLinks();
                    me.registerQuizz();
                },
                error: function(answer){
                    console.error('ooops... on view '+x+' :(');
                }
            });
        });
        $('.update_'+x).off().on('click',function(event){
            event.preventDefault();
            event.stopPropagation();
            let owner = $(this).closest('div.storyarticle').attr('id');
            let id = owner.split('_')[1];
            let form = $(this).closest('form');
            let formdata = form.serialize();
            let mode_tag = $(this).attr('mode');
            let urlupdate = x+'s/'+id+'/edit/';
            console.log("HELLO !!!");
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
                    me.co.rebootLinks();
                    $('button#'+id+'.view_'+x).click();
                    me.registerQuizz();
                },
                error: function(answer) {
                    console.log('Error... ');
                    console.log(answer);
                },
            });
        });

        $('.edit_'+x).off().on('click', function(event){
            event.preventDefault();
            event.stopPropagation();
            let t_id = $(this).attr('id')
            let id = t_id.split("_")[t_id.split("_").length-1];
            let children = $(this).parent("p").attr('children');
            let mode_tag = $(this).attr('mode');

            $.ajax({
                url: x+'s/'+id+'/edit/',
                success: function(answer) {
                    console.log(mode_tag);
                    if (mode_tag == 'overlay') {
                        $('#board').html('<div class="a"></div><div class="b" id="card_form_box"></div><div class="c"></div>');
                        $('#card_form_box').html(answer);
                        $("#board").css('display','flex');
                    }else {
                        $('#' + x + '_' + id).html(answer);
                    }
                    me.co.prepareAjax();
                    me.co.rebootLinks();
                },
                error: function(answer){
                    console.log('ooops... on edit '+x+':(');
                }
            });
        });
        $('.hide_'+x).off().on('click', function(event){
            event.preventDefault();
            event.stopPropagation();
            let t_id = $(this).attr('id')
            let id = t_id.split("_")[t_id.split("_").length-1]
            let children = $(this).parent("p").attr('children');
            $('#'+x+'_'+id).html('');
            if (children != undefined){
              let ch = children.split(";")
              _.forEach(ch,function(d){
                $("#hide_"+d).click();
              })
            }
            me.co.prepareAjax();
            me.co.rebootLinks();
            me.registerQuizz();
        });
        $('.'+x+'_update').off().on('click',function(event){
            event.preventDefault();
            event.stopPropagation();
            let owner = $(this).closest('div.storyarticle').attr('id');
            let id = owner.split('_')[1];
            let form = $(this).closest('form');
            let formdata = form.serialize();
            let urlupdate = x+'s/'+id+'/edit/';
            // console.log(urlupdate);
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
                    me.co.rebootLinks();
                    $('button#'+id+'.view_'+x).click();
                    me.registerQuizz();
                },
                error: function(answer) {
                    console.log('Error... ');
                    console.log(answer);
                },
            });
        });
        $('.add_'+x).off().on('click',function(event){
            event.preventDefault();
            event.stopPropagation();
            let id = $(this).attr("id");
            console.log(id);
            //var form = $(this).closest('form');
            let urlupdate = x+'s/add/';
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
                    me.co.rebootLinks();
                    $('#cards_list').click();
                },
                error: function(answer) {
                    console.log('Error... ');
                    console.log(answer);
                },
            });
        });
    }

    registerQuizz(){
        let me = this;
        $('.quizz').off('click').on('click',function(event){
            let id = $(this).attr('id')
            let arr_id = id.split("_")
            let quizz_id = (arr_id[0].split('x'))[1]
            let question_num = (arr_id[1].split('x'))[1]
            let answer_id = (arr_id[2].split('x'))[1]
            let tag = arr_id[3]
            $.ajax({
                url: '/ajax/quizz/'+quizz_id+'/question/'+question_num+'/tag/'+tag+'/reroll/',
                method: 'POST',
                success: function(answer){
                    console.log('Reroll!! '+id+" "+answer)
                },
                error: function(answer){
                    console.log('Something happended with '+id)
                }
            })
        });
    }

    doConnect(co){
        this.co = co;
        this.registerStory('epic');
        this.registerStory('drama');
        this.registerStory('act');
        this.registerStory('event');
        this.registerStory('adventure');
        this.registerStory('scheme');
        this.registerStory('scene');
        this.registerStory('card')
        this.registerStory('backlog');
        this.registerQuizz()
    }

}
