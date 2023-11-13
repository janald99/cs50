document.addEventListener("DOMContentLoaded", function () {
    const followButton = document.getElementById("follow-button");
    const userHeader = document.getElementById("user-header");

    // Check if the followButton element exists
    if (followButton) {
        // Function to get the initial follow state
        function getInitialFollowState() {
            return followButton.textContent.trim().toLowerCase() === "unfollow";
        }

        // Set the initial state
        var isFollowing = getInitialFollowState();

        followButton.addEventListener("click", function () {
            const username = userHeader.getAttribute("data-username");
            const action = isFollowing ? "unfollow" : "follow";

            fetch('/follow', {
                method: "POST",
                headers: {
                    "X-CSRFToken": csrfToken,
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({
                    username: username,
                    action: action,
                }),
            })
            .then(response => response.json())
            .then(data => {
                if (data.message) {
                    console.log(data.message);
                }

                const newIsFollowing = !isFollowing;
                followButton.textContent = newIsFollowing ? "Unfollow" : "Follow";

                const followersCountHeader = document.getElementById("follower-count");
                const followingCountHeader = document.getElementById("following-count");

                // Update follower and following counts
                followersCountHeader.textContent = "Followers: " + data.followersCount;
                followingCountHeader.textContent = "Following: " + data.followingCount;

                // Update the state for the next click
                isFollowing = newIsFollowing;
            });
        });
    }
});
