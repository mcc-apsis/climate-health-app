jQuery(document).ready(function($){

  var checkExist = setInterval(function() {
     if ($('.cbutton').length) {
        console.log("Exists!");
        clearInterval(checkExist);
        $(".cbutton").on('click', function(e) {
           $(this).toggleClass("clicked")
           console.log(e)
        });
        $(function () {
          $('[data-toggle="popover"]').popover()
        })
        $('.tab').click(function() {
          console.log("tab")
          $(function () {
            $('[data-toggle="popover"]').popover()
          })
        })
     }
  }, 100); // check every 100ms



});
