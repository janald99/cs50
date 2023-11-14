document.addEventListener('DOMContentLoaded', function() {
    // Function to toggle the edit container visibility
    function toggleEditContainer(postId) {
        const postElement = document.querySelector(`.post[data-post-id="${postId}"]`);
        const editContainer = postElement.querySelector('.edit-container');
        const editTextarea = postElement.querySelector('.edit-textarea');

        // Toggle visibility
        editContainer.style.display = (editContainer.style.display === 'none') ? 'block' : 'none';

        // If the edit container is visible, set the content of the textarea to the current post content
        if (editContainer.style.display === 'block') {
            editTextarea.value = postElement.querySelector('.post-content p').innerText;
        }
    }

    // Function to handle the click event on the edit button
    function handleEditButtonClick(event) {
        const postId = event.target.closest('.post').getAttribute('data-post-id');
        toggleEditContainer(postId);
    }

    // Function to handle the click event on the save edit button
    function handleSaveEditButtonClick(event) {
        const postId = event.target.closest('.post').getAttribute('data-post-id');
        const editTextarea = event.target.closest('.edit-container').querySelector('.edit-textarea');
        const editedContent = editTextarea.value;

        // Use AJAX to send the edited content to the server
        fetch(`/edit_post`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrf_token,  // Make sure to replace csrf_token with the actual token value
            },
            body: JSON.stringify({ content: editedContent , post_id: postId}),
        })
        .then(response => response.json())
        .then(data => {
            // Update the post content on success
            if (data.success) {
                const postElement = document.querySelector(`.post[data-post-id="${postId}"]`);
                postElement.querySelector('.post-content p').innerText = editedContent;
                toggleEditContainer(postId);  // Hide the edit container
            } else {
                console.error('Failed to save edited content');
            }
        });
    }

    // function handleLikeButtonClick(event) {
    //     const postId = event.target.getAttribute('data-post-id');
    //     const isLiked = event.target.getAttribute('data-is-liked') === "true";
    //     const likeCountElement = event.target.querySelector('like-count');

    //     fetch('/like_post', {
    //         method: 'POST',
    //         headers: {
    //             'Content-Type': 'application/json',
    //             'X-CSRFToken': csrf_token,
    //         },
    //         body: JSON.stringify({
    //             post_id: postId,
    //             action: isLiked ? 'unlike' : 'like',
    //         }),
    //     })
    //     .then(response => response.json())
    //     .then(data => {
    //         if (data.success) {
    //             // Update like count and button text
    //             likeCountElement.innerText = data.like_count;
    //             event.target.setAttribute('data-is-liked', (!isLiked).toString());
    //             event.target.textContent = isLiked ? 'Like' : 'Unlike';
    //         } else {
    //             console.error('Failed to toggle like');
    //         }
    //     });
    // }

    // Attach event listeners to the edit and save edit buttons
    document.querySelectorAll('.edit-post-btn').forEach(button => {
        button.addEventListener('click', handleEditButtonClick);
    });

    document.querySelectorAll('.save-edit-btn').forEach(button => {
        button.addEventListener('click', handleSaveEditButtonClick);
    });

    // Attach event listeners to the like buttons
    document.querySelectorAll('.like-button').forEach(button => {
        button.addEventListener('click', handleLikeButtonClick);
    });
});
