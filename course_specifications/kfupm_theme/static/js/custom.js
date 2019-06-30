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
            $(this).find('input[type=checkbox]').prop( "checked", true );
        }
        else{
            $(this).find('input[type=checkbox]').prop( "checked", false );
        }
    });

    //Delete adding content for submitting form
    $('body').on( "click", ".delete-adding-content", function() {
        $('.add-this').remove();
    });

    if($('.alert-popup').is(':visible')){
        var alert_popup_width = $('.alert-popup').width();
        $('.alert-popup').css("margin-left",-alert_popup_width/2);
    }

    $('body').on( "click", ".update-clo", function() {
        var clo_count = $(this).parents('.modal-footer').siblings('.modal-body').find('.select2-selection__choice').length;
        $(this).parents('.clo-sec').find('.clo-count').html(clo_count);
    });

});