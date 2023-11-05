document.addEventListener("DOMContentLoaded", function () {
    const followButton = document.getElementById("follow-button");
    const userHeader = document.getElementById("user-header");

    // Check if the followButton element exists
    if (followButton) {
        followButton.addEventListener("click", function () {
            const username = userHeader.getAttribute("data-username");
            const isFollowing = followButton.getAttribute("data-is-following") === "true";
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
                followButton.setAttribute("data-is-following", newIsFollowing.toString());
                followButton.textContent = newIsFollowing ? "Unfollow" : "Follow";

                // const followersCountHeader = document.getElementById("follower-count");
                // const followingCountHeader = document.getElementById("following-count");
                
                // console.log(typeof(updatedFollowers));
                // followersCountHeader.textContent = "Followers: " + updatedFollowers;
                // followingCountHeader.textContent ="Following: " + updatedFollowing;
            });
        });
    }
});
