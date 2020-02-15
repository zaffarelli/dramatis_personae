/*
 ╔╦╗╔═╗  ╔═╗┌─┐┬  ┬  ┌─┐┌─┐┌┬┐┌─┐┬─┐
  ║║╠═╝  ║  │ ││  │  ├┤ │   │ │ │├┬┘
 ═╩╝╩    ╚═╝└─┘┴─┘┴─┘└─┘└─┘ ┴ └─┘┴└─
*/
class Optimizer{
    constructor(){
    }

    register_duel(){
        let me = this;
        $('#run_duel').off().on('click', function(event){
            event.preventDefault();
            event.stopPropagation();
            let t_id = $(this).attr('id');
            let who = $('#customize').val();
            $('#customize').val("");
            console.log(who);
            let a = 151;
            let b = 91;
            if (who != ''){
                let x = who.split(" ");
                a = parseInt(x[0]);
                b = parseInt(x[1]);
            }
            $.ajax({
                url: 'duel/'+a+'/'+b+'/run',
                success: function(answer) {
                    $('.details').html(answer);
                    prepare_ajax();
                    rebootlinks();
                },
                error: function(answer){
                    console.log('ooops... on run duel ');
                }
            });
        });
    }

    doConnect(){
        this.register_duel();
    }
}
