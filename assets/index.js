jQuery(document).ready(function($){

  var checkExist = setInterval(function() {
     if ($('.cbutton').length) {
        console.log("Exists!");
        clearInterval(checkExist);
        $(".cbutton").on('click', function(e) {
           $(this).toggleClass("clicked")
           console.log(e)
        });
     }
  }, 100); // check every 100ms

});
