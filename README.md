## About my Project
This project is a front-end application for an email client that makes API calls to send and receive emails.

## My feature requirements
- **Send Mail:**
  - JavaScript code to send an email upon form submission.
  - Use a POST request to `/emails` with recipient, subject, and body values.
  - Redirect to the user’s sent mailbox after sending the email.

- **Mailbox:**
  - Load the Inbox, Sent mailbox, or Archive on user visit.
  - GET request to `/emails/<mailbox>` for mailbox-specific emails.
  - Query API for the latest emails in the mailbox.
  - Display mailbox name at the top of the page.
  - Render emails in boxes showing sender, subject, timestamp.
  - Unread emails: white background; read emails: gray background.

- **View Email:**
  - GET request to `/emails/<email_id>` to view email content.
  - Show sender, recipients, subject, timestamp, and body.
  - Additional div in `inbox.html` to display the email.
  - Hide/show views based on navigation options.

- **Archive and Unarchive:**
  - Allow archiving/unarchiving received emails.
  - Inbox email: button for archiving; Archive email: button for unarchiving (not in Sent mailbox).
  - PUT request to mark an email as archived or unarchived.
  - Redirect to the user’s inbox after the action.

- **Reply:**
  - Enable replying to an email.
  - Show “Reply” button while viewing an email.
  - Redirect to the email composition form on clicking “Reply.”
  - Prefill recipient, subject line (prepend Re:), and body with original email content.

## How to run the application

1. **Clone the Project Repository:**
    ```bash
    git clone https://github.com/me50/janald99.git
    cd <your_project_folder>
    ```
    At the main project directory level, you should be able to see files like manage.py, and folders like mail and project3.

2. **Navigate to Capstone branch:**
    ```bash
    git checkout web50/projects/2020/x/capstone
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
