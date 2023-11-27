document.addEventListener('DOMContentLoaded', function() {
    console.log("hey");
    // Function to toggle the edit container visibility
    function toggleEditContainer() {
        const editContainer = document.querySelector('.edit-container');
        const editTextarea = document.querySelector('.edit-textarea');

        // Toggle visibility
        editContainer.style.display = (editContainer.style.display === 'none') ? 'block' : 'none';

        // If the edit container is visible, set the description of the textarea to the current show description
        if (editContainer.style.display === 'block') {
            editTextarea.value = document.querySelector('.show-description p').innerText;
        }
    }

    // Function to handle the click event on the save edit button
    function handleSaveEditButtonClick(event) {
        event.preventDefault();

        const showElement = document.querySelector('.show');
        const showId = showElement.getAttribute('data-show-id');

        const editTextarea = document.querySelector('.edit-textarea');
        const editedDescription = editTextarea.value;

        // Use AJAX to send the edited description to the server
        fetch(`/edit_show`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrf_token,  // Make sure to replace csrf_token with the actual token value
            },
            body: JSON.stringify({ description: editedDescription , show_id: showId}),
        })
        .then(response => response.json())
        .then(data => {
            // Update the show description on success
            if (data.success) {
                document.querySelector('.show-description p').innerText = editedDescription;
                toggleEditContainer();  // Hide the edit container
            } else {
                console.error('Failed to save edited description');
            }
        });
    }
      
    // Attach event listener to the edit button
    const editShowbutton = document.querySelector('.edit-show-btn');
    editShowbutton.addEventListener('click', toggleEditContainer);
 
    // Attach event listener to the save edit button
    const saveEditbutton = document.querySelector('.save-edit-btn');
    saveEditbutton.addEventListener('click', handleSaveEditButtonClick);
});
