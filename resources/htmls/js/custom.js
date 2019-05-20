//Preloader
// $(window).load(function () {
//     $('.preloader').fadeOut(500);


// });
$(document).ready(function($) {

	// $('#multiple-checkboxes').multiselect({
 //      includeSelectAllOption: true,
 //    });
    $('.selectpicker').selectpicker();

    // $('.select-two').select2();


    //Add multiple
    $('body').on( "click", ".add-button", function() {
    	var this_has_add_content = $(this).parents('.has-add-content');
    	var this_add_this = this_has_add_content.find('.add-this').html();
    	var this_add_here = this_has_add_content.find('.add-here');
    	this_add_here.append(this_add_this);
    });

    //Delete this
    $('body').on( "click", ".delete-btn", function() {
    	var delete_this = $(this).parents('.delete-this');
    	delete_this.hide();
    	if(!delete_this.is(":visible")){
    		$(this).find('.delete-check').prop( "checked", true );
    	}
    	else{
    		$(this).find('.delete-check').prop( "checked", false );
    	}
    });

});