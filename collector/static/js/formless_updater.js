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
    }
}
