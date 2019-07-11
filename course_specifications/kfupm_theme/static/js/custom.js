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

        //alert(data_target_num);
        var name_attr = this_cloned_forms.attr('name').replace(id_number, current_form_count);
        var id_attr = this_cloned_forms.attr('id').replace(id_number, current_form_count);


        this_cloned_forms.attr('name', name_attr);
        this_cloned_forms.attr('id', id_attr);

        //alert(data_target_attr);

        //Clone last content with replaced numbers
        this_add_here.append(this_last_content);

        //has-increment-val
        //var has_incerement_val = this_add_here.find('.has-increment-val');

        this_last_content.find('.has-increment-val').each(function (){

            if($(this).attr('data-target')){
                var data_target_num = $(this).attr('data-target').match(/\d+/);
                var data_target_attr = $(this).attr('data-target').replace(data_target_num, current_form_count);
                $(this).attr('data-target', data_target_attr);
            }
            if($(this).attr('id')){
                var id_modal_num = $(this).attr('id').match(/\d+/);
                var id_modal_attr = $(this).attr('id').replace(id_modal_num, current_form_count);
                $(this).attr('id', id_modal_attr);
            }
            if($(this).attr('aria-labelledby')){
                var aria_labelledby_num = $(this).attr('aria-labelledby').match(/\d+/);
                var aria_labelledby_attr = $(this).attr('aria-labelledby').replace(aria_labelledby_num, current_form_count);
                $(this).attr('aria-labelledby', aria_labelledby_attr);
            }

        });

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

    //Actual Contact hours calculation
    $('body').on('keyup', '.form-accordian input.contact_hrs', function(){
        if($(this).hasClass('lec')){
            var lec_hrs = 0;
            $('.contact_hrs.lec').each(function(){
                if($(this).val()){
                    lec_hrs += parseInt($(this).val());
                }
            });
            $('.total_lec_contact_hrs').addClass('text-dark h6 font-weight-bold').html(lec_hrs +' hrs');
        }
        if($(this).hasClass('lab')){
            var lab_hrs = 0;
            $('.contact_hrs.lab').each(function(){
                if($(this).val()){
                    lab_hrs += parseInt($(this).val());
                }
            });
            $('.total_lab_contact_hrs').addClass('text-dark h6 font-weight-bold').html(lab_hrs +' hrs');
        }
        if($(this).hasClass('tutorial')){
            var tutorial_hrs = 0;
            $('.contact_hrs.tutorial').each(function(){
                if($(this).val()){
                    tutorial_hrs += parseInt($(this).val());
                }
            });
            $('.total_tutorial_contact_hrs').addClass('text-dark h6 font-weight-bold').html(tutorial_hrs +' hrs');
        }
        if($(this).hasClass('practical')){
            var practical_hrs = 0;
            $('.contact_hrs.practical').each(function(){
                if($(this).val()){
                    practical_hrs += parseInt($(this).val());
                }
            });
            $('.total_practical_contact_hrs').addClass('text-dark h6 font-weight-bold').html(practical_hrs +' hrs');
        }
        if($(this).hasClass('other')){
            var other_hrs = 0;
            $('.contact_hrs.other').each(function(){
                if($(this).val()){
                    other_hrs += parseInt($(this).val());
                }
            });
            $('.total_other_contact_hrs').addClass('text-dark h6 font-weight-bold').html(other_hrs +' hrs');
        }

        var total_contact_hrs = lec_hrs+lab_hrs+tutorial_hrs+practical_hrs+other_hrs;
        $('.total_contact_hrs').addClass('text-dark h6 font-weight-bold').html(total_contact_hrs +' hrs');

    });

});