// document.addEventListener('DOMContentLoaded', function() {
//   const addShowForm = document.querySelector('#add-show-form');
//   addShowForm.addEventListener('submit', postShow);
// });

// function postShow(event) {
//   event.preventDefault();

//   const title = document.querySelector('#add-show-title').value;
//   const genre = document.querySelector('#add-show-genre').value;
//   const description = document.querySelector('#add-show-description').value;
//   const imageUrl = document.querySelector('#add-show-image').value;

//   // Send a post request to /add_show to add a new show
//   fetch('/new_show', {
//       method: 'POST',
//       body: JSON.stringify({
//           title: title,
//           genre: genre,
//           description: description,
//           image_url: imageUrl
//       }),
//   })
//   .then(response => response.json())
//   .then(result => {
//       console.log(result.message);
//       clearFormFields();
//   })
//   .catch(error => {
//       console.error('Error:', error);
//   });
// }

// function clearFormFields() {
//   document.querySelector('#add-show-title').value = '';
//   document.querySelector('#add-show-genre').value = '';
//   document.querySelector('#add-show-description').value = '';
//   document.querySelector('#add-show-image').value = '';
// }
