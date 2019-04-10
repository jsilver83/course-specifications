//Preloader
// $(window).load(function () {
//     $('.preloader').fadeOut(500);


// });
$(document).ready(function($) {

    $(".clickable tr").click(function() {
        window.document.location = $(this).data("href");
    });


    //Overlay alert message alignment
    var overlay_alert_width = $('.overlay-alert').width();
    $('.overlay-alert').css('margin-left',-overlay_alert_width/2);
});