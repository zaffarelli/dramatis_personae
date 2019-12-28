class FormlessUpdater{
	constructor(){
		this.avatar = '';
		this.form = '';
		this.customizer = '';
	}

	reset(target_avatar, form, customizer){
		this.avatar = target_avatar;
		this.form = form;
		this.customizer = customizer;
		this.prepareEvents()
		console.log("RESET: "+this.form+" "+this.avatar+" "+this.customizer);
	}

	prepareEvents(){
		console.debug("Preparing Events");
		let self = this;
		this.doConnect("ba",true);
		this.doConnect("bc",true);
		this.doConnect("skill");
	}

	doConnect(prefix,symetric=false){
		let self = this;
		$("#"+prefix+"_add").off("click").on("click",function(e){
		    let i = $("#"+prefix+"_select :selected");
            let anurl = 'ajax/character/add/'+prefix+"/"+self.avatar+"/"+i.val()+'/';
            $("#"+prefix+"_block_"+self.avatar).addClass("working");
            console.log(anurl);

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
                    self.prepareEvents();
                    rebootlinks();
		 	    },
                error: function(answer){
                    console.log(answer.responseText);
                    rebootlinks();
		 	    }
	 	    });
	    });
        if (symetric == true){
            $("#"+prefix+"_del").off("click").on("click",function(e){
    		    let i = $("#"+prefix+"_unselect :selected");
                let anurl = 'ajax/character/del/'+prefix+"/"+self.avatar+"/"+i.val()+'/';
                console.log(anurl);
                $("#"+prefix+"_block_"+self.avatar).addClass("working");
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
                        self.prepareEvents();
                        rebootlinks();
    		 	    },
                    error: function(answer){
                        console.log(answer.responseText);
                        rebootlinks();
    		 	    }
    	 	    });
    	    });
        }
        $('span.skill_pick').off().on('click',function(event){
            block = $(this).parent();
            idarr = $(this).attr('id').split('_');
            skill_id = idarr[2]
            avatar_id = idarr[1]
            fingerval = 0;
            if ($(this).hasClass('fa-plus-circle')){
                fingerval = 1;
            }
            if ($(this).hasClass('fa-minus-circle')){
                fingerval = -1;
            }
            $.ajax({
                url: 'ajax/character/pick/skill/'+avatar_id+'/'+skill_id+'/',
                method: 'POST',
                headers: {
                    'Accept': 'application/json',
                    'Content-Type': 'application/x-www-form-urlencoded'
                },
                dataType:'json',
                data: {skill:skill_id,finger:fingerval},
                success: function(answer) {
                    console.log(answer);
                    $("#"+prefix+"_block_"+answer.c["id"]).html(answer.block);
                    $("#"+prefix+"_custo_block").html(answer.custo_block);
                    $("#"+prefix+"_block_"+answer.c["id"]).removeClass("working");
                },
                error: function(answer){
                    console.log(answer);
                    $('th#'+target).html(answer.responseText);
                },
            });
        });

    }
}
