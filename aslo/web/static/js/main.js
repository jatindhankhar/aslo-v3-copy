$(window).scroll(function() {
  if ($(document).scrollTop() > 10) {
    $('header').removeClass('large').addClass('small');
  } else {
    $('header').addClass('large').removeClass('small');
  }
}); 

$(function(){
  
  $(".dropdown-menu li ").click(function(){
   var actual_query =  $(this).attr("value");
   var translated_query = $(this).children("a").text();
    //console($(this).child.text());
    $(".btn:first-child").text(translated_query);
     $(".btn:first-child").val(actual_query);
     $('input[name="category-option"]').val(translated_query.trim().toLowerCase());
     $('input[name="category-option-query').val(actual_query.trim().toLowerCase());
  });

});