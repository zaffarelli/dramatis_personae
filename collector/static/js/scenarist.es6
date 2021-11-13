/*
 ╔╦╗╔═╗  ╔═╗┌─┐┬  ┬  ┌─┐┌─┐┌┬┐┌─┐┬─┐
  ║║╠═╝  ║  │ ││  │  ├┤ │   │ │ │├┬┘
 ═╩╝╩    ╚═╝└─┘┴─┘┴─┘└─┘└─┘ ┴ └─┘┴└─
*/
class Scenarist{
    constructor(){
    }

    registerStory(x){
        let me = this;
        /* Register all the actions for the scenarist items */
        $('.view_'+x).off().on('click', function(event){
            event.preventDefault();
            event.stopPropagation();
            let t_id = $(this).attr('id')
            let id = t_id.split("_")[t_id.split("_").length-1]
            let children = $(this).parent("p").attr('children');
            //$(this).css('border-color','red');
            $.ajax({
                url: x+'s/'+id+'/view/',
                success: function(answer) {
                    $('#'+x+'_'+id).html(answer);
                    if (children != undefined){
                      let ch = children.split(";")
                      _.forEach(ch,function(d){
                          $("#view_"+d).click();
                      })
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
        $('.edit_'+x).off().on('click', function(event){
            event.preventDefault();
            event.stopPropagation();
            let t_id = $(this).attr('id')
            let id = t_id.split("_")[t_id.split("_").length-1]
            let children = $(this).parent("p").attr('children');
            $.ajax({
                url: x+'s/'+id+'/edit/',
                success: function(answer) {
                    $('#'+x+'_'+id).html(answer);
                    me.co.prepareAjax();
                    me.co.rebootLinks();
                },
                error: function(answer){
                    console.log('ooops... on edit '+x+':(');
                }
            });
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
            var id = $(this).parent('p').prop('className');
            console.log(id);
            //var form = $(this).closest('form');
            var urlupdate = x+'s/add/';
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
                    //$('button#'+id+'.view_'+x).click();
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
        this.registerQuizz()
    }

}
