$(window).scroll(function() {
  if ($(document).scrollTop() > 10) {
    $('header').removeClass('large').addClass('small');
  } else {
    $('header').addClass('large').removeClass('small');
  }
});