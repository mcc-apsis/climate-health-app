
jQuery(document).ready(function($){
  function has_scrolled() {
    if ($("#regions-heading").offset().top < $(window).scrollTop() + $(window).height()/3) {
      var headingBottom = $("#regions-heading").offset().top + $("#regions-heading").outerHeight()
      if (headingBottom < $(window).scrollTop()) {
        var scrollBottom = $(window).scrollTop() + $("#sidebar").outerHeight();
        if ($("#topic-heading").offset().top < scrollBottom) {
          if ($("#topic-heading").offset().top < $(window).scrollTop() + $(window).height()/3) {
            $("#nav-regions").removeClass("active")
            $("#nav-topics").addClass("active")
          } else {
            $("#nav-regions").addClass("active")
            $("#nav-topics").removeClass("active")
          }
          var newTop = $("#topic-heading").offset().top - $(window).scrollTop() - $("#sidebar").outerHeight()
          $("#sidebar").css({"top": newTop})
        } else {
          $("#sidebar").css({"top": 0})
        }
      } else {
        if ($("#sidebar").hasClass("inView")) {
          $("#sidebar").css({"top":headingBottom - $(window).scrollTop()})
        } else {
          $("#sidebar")
            .addClass("inView")
            .animate({"top": headingBottom - $(window).scrollTop()});
          $("#nav-regions").addClass("active")
        }
      }
    } else {
      if ($("#sidebar").hasClass("inView")) {
        $("#sidebar")
          .removeClass("inView")
          .animate({"top": 1200});
        $("#nav-regions").removeClass("active")
      }
    }
  }
  $(window).on('scroll resize', has_scrolled);
  $(window).trigger('scroll');
});
