
jQuery(document).ready(function($){
  function has_scrolled() {
    // Are we in at least the regions section?
    if ($("#regions-heading").offset().top < $(window).scrollTop() + $(window).height()/3) {
      var headingBottom = $("#regions-heading").offset().top + $("#regions-heading").outerHeight()
      // Is the regions heading still in view?
      if (headingBottom > $(window).scrollTop()) {
        // Either animate it to the top, or just place it to the top if it has already been animated
        if ($("#sidebar").hasClass("inView")) {
          $("#sidebar").css({"top": headingBottom - $(window).scrollTop()})
        } else {
          $("#sidebar")
            .addClass("inView")
            .animate({"top": headingBottom - $(window).scrollTop()});
          $("#nav-regions").addClass("active")
        }
      } else {
        var scrollBottom = $(window).scrollTop() + $("#sidebar").outerHeight();
        // Section three
        if ($("#topic-heading").offset().top < scrollBottom) {
          if ($("#topic-heading").offset().top < $(window).scrollTop() + $(window).height()/3) {
            $(".nav-link").removeClass("active")
            $("#nav-topics").addClass("active")
          } else {
            $(".nav-link").removeClass("active")
            $("#nav-pathways").addClass("active")
          }
          var newTop = $("#topic-heading").offset().top - $(window).scrollTop() - $("#sidebar").outerHeight()
          $("#sidebar").css({"top": newTop})
        }  else if ($("#pathways-heading").offset().top < scrollBottom) {
          if ($("#pathways-heading").offset().top < $(window).scrollTop() + $(window).height()/3) {
            $(".nav-link").removeClass("active")
            $("#nav-pathways").addClass("active")
            var h2Bottom = $("#pathways-heading").offset().top + $("#pathways-heading").outerHeight()
            if (h2Bottom < $(window).scrollTop()) {
              $("#sidebar").css({"top": 0})
            } else{
              $("#sidebar").css({"top": h2Bottom - $(window).scrollTop()})
            }

          } else {
            $(".nav-link").removeClass("active")
            $("#nav-regions").addClass("active")
            var newTop = $("#pathways-heading").offset().top - $(window).scrollTop() - $("#sidebar").outerHeight()
            $("#sidebar").css({"top": newTop}).removeClass("inView")
          }
        } else {
          $("#sidebar").css({"top": 0})
        }
      }
    } else {
      if ($("#sidebar").hasClass("inView")) {
        $("#sidebar")
          .removeClass("inView")
          .animate({"top": $(window).height()});
        $(".nav-link").removeClass("active")
      } else {
        $("#sidebar").css({"top": $(window).height()})
      }
    }
  }
  $(window).on('scroll resize', has_scrolled);
  $(window).trigger('scroll');
});
