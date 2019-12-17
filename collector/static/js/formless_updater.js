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
		this.doConnect("ba");
		this.doConnect("bc");
		this.doConnect("skill");
	}

	doConnect(prefix){
		let self = this;
		$("#"+prefix+"_add").off("click");
		$("#"+prefix+"_add").on("click",function(e){
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
                    /*
			 		$(prefix+'_block_'+answer.id).html(answer.block);
					$(prefix+'_block_'+answer.id).html(answer.block);
			 		self.reset(answer.id,"sheet_"+answer.id,"customizer");
                    */

                    console.log(answer.avatar);
                    console.log(answer.item);
			 	    update_messenger();
		 	    },
                error: function(answer){
//                    $("#messenger").html(answer.responseText);
                    console.log(answer.responseText);
		 	    }
	 	    });
	    });
        //console.log("  >> Adding "+prefix+" ["+i.text()+" / "+i.val()+"] to avatar "+self.avatar);
    }
}
