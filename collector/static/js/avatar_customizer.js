/*
 ╔╦╗╔═╗  ╔═╗┌─┐┬  ┬  ┌─┐┌─┐┌┬┐┌─┐┬─┐
  ║║╠═╝  ║  │ ││  │  ├┤ │   │ │ │├┬┘
 ═╩╝╩    ╚═╝└─┘┴─┘┴─┘└─┘└─┘ ┴ └─┘┴└─
*/
class AvatarCustomizer{
	constructor(){
		this.avatar = '';
		this.form = '';
		this.customizer = '';
		this.co = null;
	}

	reset(target_avatar, form, customizer){
		this.avatar = target_avatar;
		this.form = form;
		this.customizer = customizer;
		this.co = co
		this.prepareEvents()
		console.log("RESET: "+this.form+" "+this.avatar+" "+this.customizer);
	}

	prepareEvents(co=null){
		console.debug("Preparing Events");
		let me = this;
		if (co != null){
		    me.co = co;
		}
		me.doConnect("ba",true);
		me.doConnect("bc",true);
		me.doConnect("skill");
        me.doConnect("weapon",true);
        me.doConnect("armor",true);
        me.doConnect("shield",true);
        me.doConnect("ritual",true);
	}

	doConnect(prefix,symetric=false){
		let me = this;
		$("#"+prefix+"_add").off("click").on("click",function(e){
		    let i = $("#"+prefix+"_select :selected");
            let anurl = 'ajax/character/add/'+prefix+"/"+me.avatar+"/"+i.val()+'/';
            let ff = $("#freefield").val();
            $("#"+prefix+"_block_"+me.avatar).addClass("working");
            console.log(anurl);
            console.log(ff);

   		    $.ajax({
                url: anurl,
                method: 'POST',
                headers: {
                    'Accept': 'application/json',
                    'Content-Type': 'application/x-www-form-urlencoded'
                },
                dataType: 'json',
                data:{'freefield':ff},
			    success: function(answer) {
                    $("#"+prefix+"_block_"+answer.c["id"]).html(answer.block);
                    $("#"+prefix+"_custo_block").html(answer.custo_block);
                    $("#"+prefix+"_block_"+answer.c["id"]).removeClass("working");
                    $("#summary_block").html(answer.summary);
                    $("li#"+answer.c["id"]).html(answer.avatar_link);
                    me.prepareEvents();
                    me.co.rebootLinks();
		 	    },
                error: function(answer){
                    console.log(answer.responseText);
                    me.co.rebootLinks();
		 	    }
	 	    });
	    });
        if (symetric == true){
            $("#"+prefix+"_del").off("click").on("click",function(e){
    		    let i = $("#"+prefix+"_unselect :selected");
                let anurl = 'ajax/character/del/'+prefix+"/"+me.avatar+"/"+i.val()+'/';
                console.log(anurl);
                $("#"+prefix+"_block_"+me.avatar).addClass("working");
       		    $.ajax({
                    url: anurl,
                    method: 'POST',
                    headers: {
                        'Accept': 'application/json',
                        'Content-Type': 'application/x-www-form-urlencoded'
                    },
                    dataType: 'json',
    			    success: function(answer) {
                        $("#"+prefix+"_block_"+answer.c["id"]).html(answer.block);
                        $("#"+prefix+"_custo_block").html(answer.custo_block);
                        $("#"+prefix+"_block_"+answer.c["id"]).removeClass("working");
                        $("#summary_block").html(answer.summary);
                        $("li#"+answer.c["id"]).html(answer.avatar_link);
                        console.log("li#"+answer.c["id"]);
                        me.prepareEvents();
                        me.co.rebootLinks();
    		 	    },
                    error: function(answer){
                        console.log(answer.responseText);
                        me.co.rebootLinks();
    		 	    }
    	 	    });
    	    });
        }
        $('span.skillpick').off().on('click',function(event){
            let idarr = $(this).attr('id').split('_');
            let avatar_id = idarr[1]
            let skill_id = idarr[2]
            let fingerval = 0;
            if ($(this).hasClass('fa-plus-circle')){
                fingerval = 51;
            }
            if ($(this).hasClass('fa-minus-circle')){
                fingerval = 49;
            }
            console.log("sk_"+skill_id)
            $("#sk_"+skill_id).addClass("working");
            $.ajax({
                url: 'ajax/character/pick/skill/'+avatar_id+'/'+skill_id+'/'+fingerval+'/',
                method: 'POST',
                headers: {
                    'Accept': 'application/json',
                    'Content-Type': 'application/x-www-form-urlencoded'
                },
                dataType:'json',
                success: function(answer) {
                    console.log(answer);
                    $("#sk_"+skill_id).removeClass("working");
                    $("#sk_"+skill_id).html(answer.block);
                    $("#summary_block").html(answer.summary);
                    $("li#"+answer.c["id"]).html(answer.avatar_link);
                    me.prepareEvents();
                    me.co.rebootLinks();
                },
                error: function(answer){
                    console.log(answer);
                    $("#sk_"+skill_id).html(answer.block);
                    me.prepareEvents();
                    me.co.rebootLinks();
                },
            });
        });

        $('span.attrpick').off().on('click',function(event){
            let idarr = $(this).attr('id').split('_');
            let avatar_id = idarr[1]
            let attr_id = idarr[2]+"_"+idarr[3]
            console.log($(this).attr('id'));
            let fingerval = 0;
            if ($(this).hasClass('fa-plus-circle')){
                fingerval = 51;
            }
            if ($(this).hasClass('fa-minus-circle')){
                fingerval = 49;
            }
            $("#"+attr_id+"_"+avatar_id).addClass("working");
            console.log("#"+attr_id+"_"+avatar_id);
            $.ajax({
                url: 'ajax/character/pick/attr/'+avatar_id+'/'+attr_id+'/'+fingerval+'/',
                method: 'POST',
                headers: {
                    'Accept': 'application/json',
                    'Content-Type': 'application/x-www-form-urlencoded'
                },
                dataType:'json',
                success: function(answer) {
                    console.log(answer);
                    $("#"+attr_id+"_"+avatar_id).removeClass("working");
                    $("#"+attr_id+"_"+avatar_id).html(answer.block);
                    $("#summary_block").html(answer.summary);
                    $("li#"+answer.c["id"]).html(answer.avatar_link);
                    console.log("li#"+answer.c["id"]);
                    me.prepareEvents();
                    me.co.rebootLinks();
                },
                error: function(answer){
                    console.log(answer);
                    //$("#sk_"+skill_id).html(answer.block);
                    me.prepareEvents();
                    me.co.rebootLinks();
                },
            });
        });



    }
}
