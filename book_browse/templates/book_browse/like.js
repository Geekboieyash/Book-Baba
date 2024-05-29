$(document).ready(function() {
    $('.like-button').click(function() {
      var bookId = $(this).data('bookId');
  
      $.ajax({
        url: '/like-book/' + bookId + '/',
        type: 'POST',
        success: function(response) {
          // Update like count UI based on response (if successful)
          var likeCountElement = $(this).find('.like-count');
          likeCountElement.text(response.likeCount);
          // Consider adding visual feedback (e.g., change button text/color)
        },
        error: function(error) {
          console.error("Error liking book:", error);
          // Handle errors (e.g., display error message)
        }
      });
    });
  });
  