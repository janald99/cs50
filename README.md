## About my Project
This project features a Twitter-like social network website for making posts and following users.

## My feature requirements
- **New Post:**
  - Signed-in users can create new text-based posts.
  - Option to create a separate page or integrate the “New Post” feature on the “All Posts” page.

- **All Posts:**
  - “All Posts” link leads to a page displaying all user posts, newest first.
  - Includes poster’s username, post content, post date/time, and post “likes” (initially 0).

- **Profile Page:**
  - Clicking a username navigates to the user’s profile.
  - Displays follower count, following count, and user’s posts in reverse chronological order.
  - Shows “Follow”/“Unfollow” button for other users, excluding the signed-in user.

- **Following:**
  - “Following” link leads to a page with posts from users the current user follows.
  - Behavior is similar to the “All Posts” page, but with a restricted set of posts.
  - Accessible only for signed-in users.

- **Pagination:**
  - Display only 10 posts per page.
  - Use “Next” and “Previous” buttons for navigation between post pages.

- **Edit Post:**
  - Users can edit their own posts using an “Edit” button/link.
  - Enables editing post content in a textarea without a full page reload.
  - Ensure user-specific editing; prevent users from editing others’ posts.

- **“Like” and “Unlike”:**
  - Allow users to toggle “like” status on any post.
  - Use JavaScript for asynchronous updates to the server, updating like counts without full page reloads.


## How to run the application

1. **Clone the Project Repository:**
    ```bash
    git clone https://github.com/me50/janald99.git
    cd <your_project_folder>
    ```
    At the main project directory level, you should be able to see files like manage.py, and folders like network and project4.

2. **Navigate to Network branch:**
    ```bash
    git checkout web50/projects/2020/x/network
    ```

3. **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
4. **Database Migrations:**
    ```bash
    python manage.py makemigrations
    python manage.py migrate
    ```

5. **Create a Superuser (Admin):**
    ```bash
    python manage.py createsuperuser
    # Follow the prompts to create a superuser account
    ```

6. **Run the Development Server:**
    ```bash
    python manage.py runserver
    ```

7. **Access the Application:**
    Open a web browser and visit `http://127.0.0.1:8000/` to view the application.
    
7. **Access the Admin Interface:**
    - Go to `http://127.0.0.1:8000/admin/` and log in using the superuser credentials created earlier.
    - Use the Django admin interface to manage users, shows, and other data.
