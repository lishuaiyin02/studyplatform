var FormWizard = function () {
    return {
        init: function () {
            if (!jQuery().bootstrapWizard) {
                return;
            }
			/*-----------------------------------------------------------------------------------*/
			/*	Show country list in Uniform style
			/*-----------------------------------------------------------------------------------*/
            $("admin").select2({
                placeholder: "选择admin方式"
            });

            var wizform = $('#wizForm');
			var alert_success = $('.alert-success', wizform);
            var alert_error = $('.alert-danger', wizform);
            
			/*-----------------------------------------------------------------------------------*/
			/*	Validate the form elements
			/*-----------------------------------------------------------------------------------*/
            wizform.validate({
                doNotHideMessage: true,
				errorClass: 'error-span',
                errorElement: 'span',
                rules: {
                    /* Create Account */
					fit: {
                        required: true
                    },
                    admin: {
                        required: true
                    },
                    dose: {
                        required: true
                    },
                    utime: {
                        required: true
                    },
                    uconc: {
                        required: true
                    },
                    udose: {
                        required: true
                    },
                    fileupload: {
                        required: true
                    }
                },

                invalidHandler: function (event, validator) { 
                    alert_success.hide();
                    alert_error.show();
                },

                highlight: function (element) { 
                    $(element)
                        .closest('.form-group').removeClass('has-success').addClass('has-error'); 
                },

                unhighlight: function (element) { 
                    $(element)
                        .closest('.form-group').removeClass('has-error'); 
                },

                success: function (label) {
                    if (label.attr("for") == "gender") { 
                        label.closest('.form-group').removeClass('has-error').addClass('has-success');
                        label.remove(); 
                    } else { 
                        label.addClass('valid') 
                        .closest('.form-group').removeClass('has-error').addClass('has-success'); 
                    }
                }
            });

            /*-----------------------------------------------------------------------------------*/
			/*	Initialize Bootstrap Wizard
			/*-----------------------------------------------------------------------------------*/
            $('#formWizard').bootstrapWizard({
                'nextSelector': '.nextBtn',
                'previousSelector': '.prevBtn',
                onNext: function (tab, navigation, index) {
                    alert_success.hide();
                    alert_error.hide();
                    if (wizform.valid() == false) {
                        return false;
                    }
                    var total = navigation.find('li').length;
                    var current = index + 1;
                    $('.stepHeader', $('#formWizard')).text('Step ' + (index + 1) + ' of ' + total);
                    jQuery('li', $('#formWizard')).removeClass("done");
                    var li_list = navigation.find('li');
                    for (var i = 0; i < index; i++) {
                        jQuery(li_list[i]).addClass("done");
                    }
                    if (current == 1) {
                        $('#formWizard').find('.prevBtn').hide();
                    } else {
                        $('#formWizard').find('.prevBtn').show();
                    }
                    if (current >= total) {
                        $('#formWizard').find('.nextBtn').hide();
                        $('#formWizard').find('.submitBtn').show();
                    } else {
                        $('#formWizard').find('.nextBtn').show();
                        $('#formWizard').find('.submitBtn').hide();
                    }
                },
                onPrevious: function (tab, navigation, index) {
                    alert_success.hide();
                    alert_error.hide();
                    var total = navigation.find('li').length;
                    var current = index + 1;
                    $('.stepHeader', $('#formWizard')).text('Step ' + (index + 1) + ' of ' + total);
                    jQuery('li', $('#formWizard')).removeClass("done");
                    var li_list = navigation.find('li');
                    for (var i = 0; i < index; i++) {
                        jQuery(li_list[i]).addClass("done");
                    }
                    if (current == 1) {
                        $('#formWizard').find('.prevBtn').hide();
                    } else {
                        $('#formWizard').find('.prevBtn').show();
                    }
                    if (current >= total) {
                        $('#formWizard').find('.nextBtn').hide();
                        $('#formWizard').find('.submitBtn').show();
                    } else {
                        $('#formWizard').find('.nextBtn').show();
                        $('#formWizard').find('.submitBtn').hide();
                    }
                },
				onTabClick: function (tab, navigation, index) {
                    //bootbox.alert('On Tab click is disabled');
                    return false;
                },
                onTabShow: function (tab, navigation, index) {
                    var total = navigation.find('li').length;
                    var current = index + 1;
                    var $percent = (current / total) * 100;
                    $('#formWizard').find('.progress-bar').css({
                        width: $percent + '%'
                    });
                    if(current==3){
                    	$("p[data-display]").each(function(){
                    		console.log("aaaa");
                    		var t = $(this).attr("data-display") ;
							
                    		if(t=="admin"){
                    			$("select[name='admin']").val();
                    			
                    			$(this).text($("select[name='admin']").find("option:selected").text());
                    		}
 /*                   		else if(t=="fit"){
                    			selector = "input[name='"+ t +"']:checked";
                    			console.log(selector);
                    			$(this).text($(selector).val());
                    		}*/
                    		else{
                    			selector = "input[name='"+ t +"']";
                    			console.log(selector);
                    			$(this).text($(selector).val());
                    		}
                    		
                    	});
                    	
                    }
                }
            });

            $('#formWizard').find('.prevBtn').hide();
            $('#formWizard .submitBtn').click(function () {
                bootbox.alert("表单提交成功.");
            }).hide();
        }
    };
}();

$("#country_select").change(function (e) { 
    e.preventDefault();
    //alert($(this).val());
    if ($(this).val()=="Extravascular"){
    $("#dur_group").removeClass("hidden");
    }
    else{
        $("#dur_group").addClass("hidden");
    }    
    
});
