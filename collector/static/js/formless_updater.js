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
		//console.log(this.form+" "+this.avatar+" "+this.customizer);
		this.prepareEvents()
		console.log("RESET: "+this.form+" "+this.avatar+" "+this.customizer);
	}

	prepareEvents(){
		console.debug("Preparing Events");
		let self = this
		this.doConnect("ba")
		this.doConnect("bc")
		this.doConnect("skill")
		/*
		$("#ba_add").off("click")
		$("#ba_add").on("click",function(e){
			$("#ba_select").css("border","1px solid red");
			var i = $("#ba_select :selected");
			//var x = $("#ba_select").options[i].text;
			console.log("Adding b/a ["+i.text()+" / "+i.val()+"] to avatar "+self.avatar);
		});
		*/
	}

	doConnect(prefix){
		let self = this
		$("#"+prefix+"_add").off("click")
		$("#"+prefix+"_add").on("click",function(e){
			var i = $("#"+prefix+"_select :selected");
   		$.ajax({
				url: 'ajax/character/'+prefix+"/"+self.avatar+'/',
				success: function(answer) {
			 		$(prefix+'_block_'+answer.id).html(answer.block);
					$(prefix+'_block_'+answer.id).html(answer.block);
			 		self.reset(answer.id,"sheet_"+answer.id,"customizer");
			 		update_messenger();
		 		},
		 		error: function(answer){
					console.log('Customize error...\n'+answer);
		 		}
	 		});
			console.log("  >> Adding "+prefix+" ["+i.text()+" / "+i.val()+"] to avatar "+self.avatar);
		});
	}



}
