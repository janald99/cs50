document.addEventListener('DOMContentLoaded', function() {
    const stars = document.querySelectorAll('.star');
  
    stars.forEach(star => {
      star.addEventListener('click', function() {
        const rating = this.getAttribute('data-rating');
        alert(`You rated this show ${rating} stars!`);
  
        // Here you can make an AJAX request to update the rating in the backend
        // Send the 'rating' value to the server to save the user's rating for the show
        // You'll need to implement the backend logic to update the rating in the database
        // Example AJAX request using fetch:
        // fetch(`/rate_show/${show_id}/${rating}`, {
        //   method: 'POST',
        //   // additional headers or data can be added here
        // })
        // .then(response => {
        //   // handle the response as needed
        // })
        // .catch(error => {
        //   // handle errors here
        // });
      });
    });

  });
  