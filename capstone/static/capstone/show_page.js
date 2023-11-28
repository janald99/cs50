document.addEventListener('DOMContentLoaded', function() {
    const synopsisText = document.querySelector('.synopsis-text');
    const editableContent = document.querySelector('.edit-container');
    const editTextarea = document.querySelector('.edit-textarea');

    // Function to toggle the edit container visibility
    function toggleEditContainer() {
        editableContent.style.display = (editableContent.style.display === 'none') ? 'block' : 'none';

        if (editableContent.style.display === 'block') {
            editTextarea.value = synopsisText.textContent;
        }
    }

    // Function to handle the click event on the save edit button
    function handleSaveEditButtonClick(event) {
        event.preventDefault();

        const showElement = document.querySelector('.show');
        const showId = showElement.getAttribute('data-show-id');

        const editTextarea = document.querySelector('.edit-textarea');
        const editedDescription = editTextarea.value;

        fetch(`/edit_show`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrf_token,  
            },
            body: JSON.stringify({ description: editedDescription , show_id: showId}),
        })
        .then(response => response.json())
        .then(data => {
            // Update the show description on success
            if (data.success) {
                synopsisText.textContent = editedDescription;
                toggleEditContainer();  // Hide the edit container after saving
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
