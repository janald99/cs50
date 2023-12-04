## About my Project
This project features an eBay-like e-commerce auction site that will allow users to post auction listings, place bids on listings, comment on those listings, and add listings to a “watchlist.”

## My feature requirements
- **Create Listing:**
  - Users can create new listings with a title, text-based description, and starting bid.
  - Optional: users can include an image URL and/or category (e.g., Fashion, Toys, Electronics) for the listing.

- **Active Listings Page:**
  - Default route displays all currently active auction listings.
  - For each listing, display at least the title, description, current price, and listing photo (if available).

- **Listing Page:**
  - Clicking a listing shows specific details, including the current price.
  - For signed-in users:
    - Add/Remove the item to/from their “Watchlist.”
    - Place bids meeting specified criteria.
    - Close an auction they created, making the highest bidder the winner.
    - Display winning status if the user has won a closed auction.
    - Allow users to comment on the listing.

- **Watchlist:**
  - Signed-in users can access a Watchlist page displaying added listings.
  - Clicking on a listing navigates to that listing’s page.

- **Categories:**
  - Users can view a page listing all categories.
  - Clicking on a category name leads to a page displaying active listings in that category.

- **Django Admin Interface:**
  - Admin can perform view, add, edit, and delete operations on listings, comments, and bids via the Django admin interface.



## How to run the application

1. **Clone the Project Repository:**
    ```bash
    git clone https://github.com/me50/janald99.git
    cd <your_project_folder>
    ```
    At the main project directory level, you should be able to see files like manage.py, and folders like network and project4.

2. **Navigate to Commerce branch:**
    ```bash
    git checkout web50/projects/2020/x/commerce
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
