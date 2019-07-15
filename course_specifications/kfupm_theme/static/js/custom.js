$(document).ready(function($) {

    $('.selectpicker').selectpicker();

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


        //Clone last content with replaced numbers
        this_add_here.append(this_last_content);

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


    $('.delete-this, .hours-val').addClass('active');

    //Actual Contact hours calculation
    function total_contact_hrs(){
        var total_contact_hrs = lec_hrs+lab_hrs+tutorial_hrs+practical_hrs+other_hrs;
        $('.total_contact_hrs').addClass('text-dark h6 font-weight-bold').html(total_contact_hrs +' hrs');
    }
    function contact_hrs_calc(){
        var lec_hrs = 0;
        var lab_hrs = 0;
        var tutorial_hrs = 0;
        var practical_hrs = 0;
        var other_hrs = 0;

        var active_element = $('.hours-val.active');

        active_element.find('.contact_hrs.lec').each(function(){
            if($(this).val()){
                lec_hrs += parseInt($(this).val());
                $('.total_lec_contact_hrs').addClass('text-dark h6 font-weight-bold').html(lec_hrs +' hrs');
            }
        });
        active_element.find('.contact_hrs.lab').each(function(){
            if($(this).val()){
                lab_hrs += parseInt($(this).val());
                $('.total_lab_contact_hrs').addClass('text-dark h6 font-weight-bold').html(lab_hrs +' hrs');
            }
        });
        active_element.find('.contact_hrs.tutorial').each(function(){
            if($(this).val()){
                tutorial_hrs += parseInt($(this).val());
                $('.total_tutorial_contact_hrs').addClass('text-dark h6 font-weight-bold').html(tutorial_hrs +' hrs');
            }
        });
        active_element.find('.contact_hrs.practical').each(function(){
            if($(this).val()){
                practical_hrs += parseInt($(this).val());
                $('.total_practical_contact_hrs').addClass('text-dark h6 font-weight-bold').html(practical_hrs +' hrs');
            }
        });
        active_element.find('.contact_hrs.other').each(function(){
            if($(this).val()){
                other_hrs += parseInt($(this).val());
                $('.total_other_contact_hrs').addClass('text-dark h6 font-weight-bold').html(other_hrs +' hrs');
            }
        });
        console.log(lec_hrs, lab_hrs, tutorial_hrs, practical_hrs, other_hrs);
        var total_contact_hrs = lec_hrs+lab_hrs+tutorial_hrs+practical_hrs+other_hrs;
        $('.total_contact_hrs').addClass('text-dark h6 font-weight-bold').html(total_contact_hrs +' hrs');
    }
    contact_hrs_calc();

    $('body').on('keyup', '.form-accordian input.contact_hrs', function(){
        contact_hrs_calc($(this));
    });

    //Delete this
    $('body').on( "click", ".delete-btn", function() {
        var delete_this = $(this).parents('.delete-this');
        delete_this.removeClass('active').hide();
        contact_hrs_calc();
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


    function clo_counts(){
        $('.clo-sec').each(function (){
            var added_clo_count = $(this).find('.select2-selection__choice').length;
            $(this).find('.add_clo').hide();
            if(added_clo_count < 1){
                $(this).find('.add_clo.add').show();
            }
            else{
                $(this).find('.add_clo.added').show();
                $(this).parents('.clo-sec').find('.clo-count').html(added_clo_count);
            }
        });
    }

    $('body').on( "click", ".update-clo", function() {
        // var clo_count = $(this).parents('.modal-footer').siblings('.modal-body').find('.select2-selection__choice').length;
        // $(this).parents('.clo-sec').find('.add_clo').hide();
        // $(this).parents('.clo-sec').find('.add_clo.added').show();
        // $(this).parents('.clo-sec').find('.clo-count').html(clo_count);
        clo_counts();
    });

});