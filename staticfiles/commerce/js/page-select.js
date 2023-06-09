$(document).ready(function() {
    // Add a click event listener to all li elements
    $('li').click(function() {
        console.log('kkkkkkkkkkk');
      // Remove the "active" class from all li elements
      $('li').removeClass('active');
      // Add the "active" class to the clicked li element
      $(this).addClass('active');
    });
});