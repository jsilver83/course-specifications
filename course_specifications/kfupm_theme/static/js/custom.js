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
    // $('body').on( "click", ".add-button", function() {
    //     var this_has_add_content = $(this).parents('.has-add-content');
    //     var this_add_this = this_has_add_content.find('.add-this').html();
    //     var this_add_here = this_has_add_content.find('.add-here');
    //     this_add_here.append(this_add_this);
    // });

    $('body').on( "click", ".add-button", function() {
        var this_has_add_content = $(this).parents('.has-add-content');
        var this_add_here = this_has_add_content.find('.add-here');
        var this_last_content = this_has_add_content.find('.add-here .delete-this:visible').last().clone();
        var this_cloned_forms = this_last_content.find("input, textarea");
        this_cloned_forms.val("");
        var total_forms_count = this_add_here.find("input[name*='-TOTAL_FORMS']");
        var current_form_count = parseInt(total_forms_count.val()) + 1;
        total_forms_count.val(current_form_count);
        var name_number = this_cloned_forms.attr('name').match(/\d+/);
        var id_number = this_cloned_forms.attr('id').match(/\d+/);
        var name_attr = this_cloned_forms.attr('name').replace(id_number, current_form_count);
        var id_attr = this_cloned_forms.attr('id').replace(id_number, current_form_count);
        this_cloned_forms.attr('name', name_attr);
        this_cloned_forms.attr('id', id_attr);
        //});
        this_add_here.append(this_last_content);
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

    //Increment attribute numbers while clicking add button
    // $('body').on( "click", "#nav-lecture .add-button", function(){
    //     var total_forms_count = $("input[name*='-TOTAL_FORMS']");
    //     var current_form_count = parseInt(total_forms_count.val()) + 1;
    //     total_forms_count.val(current_form_count);
    //     $('.add-here .delete-this:visible').last().find('.has-increment-val').each(function() {
    //         $.each(this.attributes, function() {
    //             if(this.specified && this.value.indexOf("increment_num") > -1) {
    //                 var selected_attr_name = this.name;
    //                 var selected_attr_val = this.value.replace('increment_num', '');
    //                 this.value = selected_attr_val+current_form_count;
    //                 //console.log(this.name, this.value);
    //             }
    //         });
    //     });
    // });

});