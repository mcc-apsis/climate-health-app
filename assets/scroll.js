
jQuery(document).ready(function($){
  function has_scrolled() {
    if ($("#regions-heading").offset().top < $(window).scrollTop() -50) {
      if ($("#sidebar").hasClass("inView")) {

      } else {
        console.log("show sidebar")
        $("#sidebar")
          .addClass("inView")
          .css({"top":1000})
          .animate({"top": 0});
      }
    } else {
      if ($("#sidebar").hasClass("inView")) {
        console.log("hide sidebar")
        $("#sidebar")
          .removeClass("inView")
          .css({"top":0})
          .animate({"top": 1200});
      }

    }
  }
  $(window).on('scroll resize', has_scrolled);
  $(window).trigger('scroll');
});
