jQuery(function($) {
  $(document).ready( function() {
      //enabling stickUp on the '.navbar-wrapper' class
      $('.navbar').stickUp();
      smoothScroll.init({
          speed: 400, // Integer. How fast to complete the scroll in milliseconds
          easing: 'easeInOutCubic', // Easing pattern to use
          updateURL: false, // Boolean. Whether or not to update the URL with the anchor hash on scroll
          offset: 100, // Integer. How far to offset the scrolling anchor location in pixels
          callbackBefore: function ( toggle, anchor ) {}, // Function to run before scrolling
          callbackAfter: function ( toggle, anchor ) {} // Function to run after scrolling
    });
    d3.select(window).on('resize', resize_window);
    $("#disclaimer1").popover({placement:'top'});
  });
});
