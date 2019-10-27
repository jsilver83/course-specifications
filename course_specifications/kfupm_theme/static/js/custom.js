function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

$(document).ready(function ($) {

    $.ajaxSetup({
        beforeSend: function (xhr, settings) {
            let csrftoken = getCookie('csrftoken');
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });

    $('.selectpicker').selectpicker();

    function select_two() {
        try {
            $('.select2').not('.add-this .select2').select2();
        } catch (e) {
        }
    }

    select_two();

    $('.add_more').click(function () {
        var this_has_add_content = $(this).parents('.has-add-content');
        var form_idx = this_has_add_content.find("input[name*='-TOTAL_FORMS']").val();
        var append_form = this_has_add_content.find('.add-this').html();
        this_has_add_content.find('.add-here').append(append_form.replace(/__prefix__/g, form_idx).replace(/__placeholder__/g, form_idx));
        this_has_add_content.find("input[name*='-TOTAL_FORMS']").val(parseInt(form_idx) + 1);

        //  list of learning outcomes limit to 7 items
            var number_of_learning_outcomes = $('#listOfLearnOutcome li:visible').length;
            var number_of_main_objective_items = $('#listmainobjectives li:visible').length;

                if (number_of_main_objective_items < 6 ){
                    $('#mainObjDelBtn').removeAttr("disabled");
                }
                  if(number_of_main_objective_items === 6){
                    $('#mainObjAddBtn').prop("disabled", true);
                }
              if (number_of_learning_outcomes < 7 ){
                    $('#outcomeDelBtn').removeAttr("disabled");
                 }
                   if(number_of_learning_outcomes === 7){
                    $('#outcomeAddBtn').prop("disabled", true);
                }

        select_two();


    });


    $('body').on("click", ".add-button", function () {
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

        this_last_content.find('.has-increment-val').each(function () {
            if ($(this).attr('data-target')) {
                var data_target_num = $(this).attr('data-target').match(/\d+/);
                var data_target_attr = $(this).attr('data-target').replace(data_target_num, current_form_count);
                $(this).attr('data-target', data_target_attr);

            }
            if ($(this).attr('id')) {
                var id_modal_num = $(this).attr('id').match(/\d+/);
                var id_modal_attr = $(this).attr('id').replace(id_modal_num, current_form_count);
                $(this).attr('id', id_modal_attr);
            }
            if ($(this).attr('aria-labelledby')) {
                var aria_labelledby_num = $(this).attr('aria-labelledby').match(/\d+/);
                var aria_labelledby_attr = $(this).attr('aria-labelledby').replace(aria_labelledby_num, current_form_count);
                $(this).attr('aria-labelledby', aria_labelledby_attr);

            }


        });

        select_two();
    });


    $('.delete-this, .hours-val').addClass('active');

    //Actual Contact hours calculation
    function total_contact_hrs() {
        var total_contact_hrs = lec_hrs + lab_hrs + tutorial_hrs + practical_hrs + other_hrs;
        $('.total_contact_hrs').addClass('text-dark h6 font-weight-bold').html(total_contact_hrs + ' hrs');
    }

    function contact_hrs_calc() {
        var lec_hrs = 0;
        var lab_hrs = 0;
        var tutorial_hrs = 0;
        var practical_hrs = 0;
        var other_hrs = 0;

        var active_element = $('.hours-val.active');

        active_element.find('.contact_hrs.lec').each(function () {
            if ($(this).val()) {
                lec_hrs += parseInt($(this).val());
                $('.total_lec_contact_hrs').addClass('text-dark h6 font-weight-bold').html(lec_hrs + ' hrs');
            }
        });
        active_element.find('.contact_hrs.lab').each(function () {
            if ($(this).val()) {
                lab_hrs += parseInt($(this).val());
                $('.total_lab_contact_hrs').addClass('text-dark h6 font-weight-bold').html(lab_hrs + ' hrs');
            }
        });
        active_element.find('.contact_hrs.tutorial').each(function () {
            if ($(this).val()) {
                tutorial_hrs += parseInt($(this).val());
                $('.total_tutorial_contact_hrs').addClass('text-dark h6 font-weight-bold').html(tutorial_hrs + ' hrs');
            }
        });
        active_element.find('.contact_hrs.practical').each(function () {
            if ($(this).val()) {
                practical_hrs += parseInt($(this).val());
                $('.total_practical_contact_hrs').addClass('text-dark h6 font-weight-bold').html(practical_hrs + ' hrs');
            }
        });
        active_element.find('.contact_hrs.other').each(function () {
            if ($(this).val()) {
                other_hrs += parseInt($(this).val());
                $('.total_other_contact_hrs').addClass('text-dark h6 font-weight-bold').html(other_hrs + ' hrs');
            }
        });
      //  console.log(lec_hrs, lab_hrs, tutorial_hrs, practical_hrs, other_hrs);
        var total_contact_hrs = lec_hrs + lab_hrs + tutorial_hrs + practical_hrs + other_hrs;
        $('.total_contact_hrs').addClass('text-dark h6 font-weight-bold').html(total_contact_hrs + ' hrs');
    }

    contact_hrs_calc();

    function self_study_contact_hrs() {
        var self_study_contact_hrs = 0;
        $('#self-study .contact_hrs input').each(function () {
            if ($(this).val()) {
                self_study_contact_hrs += parseInt($(this).val());
        //        console.log('Self study hrs', self_study_contact_hrs);
                $('#total_self_study_contact_hrs').html(self_study_contact_hrs);
            }
        });
    }

    self_study_contact_hrs();

    $('body').on('keyup', '#self-study .contact_hrs input', function () {
        self_study_contact_hrs();
    });

    $('body').on('keyup', '.form-accordian input.contact_hrs', function () {
        contact_hrs_calc($(this));
    });

    //Delete this
    $('body').on("click", ".delete-btn", function () {
        var delete_this = $(this).parents('.delete-this');
        delete_this.removeClass('active').hide();
        contact_hrs_calc();
        if (!delete_this.is(":visible")) {
            $(this).find('input[type=checkbox]').prop("checked", true);
        } else {
            $(this).find('input[type=checkbox]').prop("checked", false);
        }

        // disable delete button if form has one list item
        var number_of_learning_outcomes = $('#listOfLearnOutcome li:visible').length;
        var number_of_main_objective_items = $('#listmainobjectives li:visible').length;
        console.log(number_of_main_objective_items);
            // learning outcome validation
            if(number_of_learning_outcomes  < 7){
                 $('#outcomeAddBtn').removeAttr('disabled');
                 $('#outcomeDelBtn').removeAttr('disabled');
                }
            if(number_of_learning_outcomes === 1){
                $('#outcomeDelBtn').prop("disabled");
                }

            // main objective validation
         if(number_of_main_objective_items < 6){

                    $('#mainObjAddBtn').removeAttr('disabled');
                    $('#mainObjDelBtn').removeAttr('disabled');
            }

          if(number_of_main_objective_items === 1 ){

                 $('#mainObjDelBtn').prop('disabled', true);
            }




    });




    //Delete adding content for submitting form
    $('body').on("click", ".delete-adding-content", function () {
        $('.add-this').remove();


    });

    if ($('.alert-popup').is(':visible')) {
        var alert_popup_width = $('.alert-popup').width();
        $('.alert-popup').css("margin-left", -alert_popup_width / 2);
    }


    // function clo_counts(){
    // }

    $('body').on("click", ".update-clo", function () {
        // var clo_count = $(this).parents('.modal-footer').siblings('.modal-body').find('.select2-selection__choice').length;
        // $(this).parents('.clo-sec').find('.add_clo').hide();
        // $(this).parents('.clo-sec').find('.add_clo.added').show();
        // $(this).parents('.clo-sec').find('.clo-count').html(clo_count);
        // clo_counts();
        // $('.clo-sec').each(function (){
        var added_clo_count = $(this).parent('.modal-footer').siblings('.modal-body').find('.select2-selection__choice').length;
     //   console.log('CLO added count', added_clo_count);
        // $(this).find('.add_clo').hide();
        // if(added_clo_count < 1){
        //     $(this).find('.add_clo.add').show();
        // }
        // else{
        // $(this).find('.add_clo.added').show();
        $(this).parents('.modal').siblings('.btn').find('.clo-count').html(added_clo_count);
        // }
        // });
    });


    // $(function() {
    //     $("#touchScroller").smoothTouchScroll({ continuousScrolling: false });
    // });

    //Checklist submenu dropdown
    $('body').on("click", '.checklist-menu > .has-sub-menu .drop-btn', function () {
        $(this).parents('.has-sub-menu').toggleClass('open');
    });

    function touchscroll_height() {
        var h_window = $(window).outerHeight(true);
        var h_course_title = $('.course-title').outerHeight(true);
        var h_navbar = $('.navbar').outerHeight(true);
        var h_btn_row = $('.btn-row').outerHeight(true) + 24;
        // alert(h_btn_row + "px");
        $('.chariman-view-layout').css('height', h_window - h_navbar + "px");
        var h_chariman_view_layout = $('.chariman-view-layout').outerHeight() - 32;
        $('#touchScroller').css('height', h_chariman_view_layout - h_course_title - h_btn_row + "px");
    }

    //touchscroll_height();
    $(window).resize(function () {
        //touchscroll_height();
    });
    $('#touchScroller .card-body').css('overflow-y', 'auto');


    //Completed main menu
    function menu_completed_check() {
        $('.checklist-menu .sub-menu').each(function () {
            if ($(this).find("a.completed").length == $(this).find("a").length) {
                $(this).parents('li').addClass('completed');
            } else {
                $(this).parents('li').removeClass('completed');
            }
        });
    }

    //Card ID
    function card_id(thisObj) {
        if (thisObj.hasClass('comment-btn')) {
            var this_id = thisObj.parents('.card').attr('id');
            $('.checklist-menu').find('.' + this_id).addClass('completed with-comments');
        }
        if (thisObj.hasClass('check-btn')) {
            var this_id = thisObj.parents('.card').attr('id');
            $('.checklist-menu').find('.' + this_id).addClass('completed');
        }
        if (thisObj.hasClass('undo-btn')) {
            var this_id = thisObj.parents('.card').attr('id');
            $('.checklist-menu').find('.' + this_id).removeClass('completed with-comments');
        }
    }

    //Action button
    $('body').on("click", '.comment-btn', function () {
        var this_parent = $(this).parents('.action-section');
        this_parent.parents('.card').addClass('commented');
        card_id($(this));
        menu_completed_check();
    });
    $('body').on("click", '.check-btn', function () {
        var this_parent = $(this).parents('.action-section');
        this_parent.parents('.card').addClass('checked');
        card_id($(this));
        menu_completed_check();
    });
    $('body').on("click", '.undo-btn', function () {
        $('.action-section').find('input[type="checkbox"]').prop('checked', false);
        $(this).parents('.card').removeClass('checked commented');
        card_id($(this));
        if ($('.check-all').hasClass('active')) {
            $('.check-all').removeClass('active');
        }
        menu_completed_check();
    });


    $('body').on("click", '.check-all', function () {
        if ($(this).hasClass('active')) {
            $('.action-section').find('input[type="checkbox"]').prop('checked', false);
            $('#touchScroller .card').removeClass('commented checked');
            $('.checklist-menu').find('a').removeClass('completed with-comments');
            $(this).removeClass('active');
        } else {
            $('.action-section').find('input[type="checkbox"]').prop('checked', false);
            $('.action-section .check-btn input[type="checkbox"]').prop('checked', true);
            $('#touchScroller .card').removeClass('commented').addClass('checked');
            $(this).addClass('active');
            $('.checklist-menu .active').find('a').addClass('completed').removeClass('with-comments');
        }
        menu_completed_check();
    });

    $('.action-section input[type="checkbox"]').each(function () {
        if ($(this).prop('checked')) {
            $(this).parents('.card').removeClass('commented checked');
            var this_p_btn = $(this).parent('.btn');
            if (this_p_btn.hasClass('comment-btn')) {
                $(this).parents('.card').addClass('commented');
                var this_id = this_p_btn.parents('.card').attr('id');
                $('.checklist-menu').find('.' + this_id).addClass('completed with-comments');
            } else if (this_p_btn.hasClass('check-btn')) {
                $(this).parents('.card').addClass('checked');
                var this_id = this_p_btn.parents('.card').attr('id');
                $('.checklist-menu').find('.' + this_id).addClass('completed');
            }
        }
    });

    //menu_completed_check();

    //Chat view scroll to bottom
    if ($('#chat-scroll').is(':visible')) {
        $('#chat-scroll').animate({
            scrollTop: $('#chat-scroll').get(0).scrollHeight
        }, 500);
    }


});