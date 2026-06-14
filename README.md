# Library Management System

This is a Django-based Library Management System for browsing books, managing users, tracking borrowings, and maintaining a wishlist. The project is structured as a small web application with two main apps:

- `library` for book catalog, borrowing, reservation, wishlist, and public pages
- `accounts` for registration, login, and logout

## Project Overview

The application lets users:

- browse featured books on the home page
- search and filter books by title, author, category, and availability
- view detailed book information, including ISBN, description, cover image, and related books
- borrow books when copies are available
- reserve books or add them to a wishlist
- view personal borrowing history and saved books
- register, log in, and log out securely

## Technologies Used

- Python
- Django
- SQLite
- HTML5
- CSS3
- JavaScript
- Bootstrap 5
- Font Awesome
- Django template engine

## Architecture

The project follows the standard Django MVT pattern:

- Model: data structures in `book/library/models.py`
- View: request handlers and business logic in `book/library/views.py` and `book/accounts/views.py`
- Template: presentation layer in `book/templates/`

### Main Components

#### 1. Project Configuration

The Django project lives under `book/` and is started through `book/manage.py`. Global configuration is handled in `book/book/settings.py`, while URL routing is defined in `book/book/urls.py`.

Important settings include:

- SQLite database stored at `book/db.sqlite3`
- media uploads enabled through `MEDIA_URL` and `MEDIA_ROOT`
- static files support for CSS and JavaScript assets
- authentication redirects for login and logout flows

#### 2. Library App

The `library` app contains the core application logic.

Models:

- `Category` groups books into genres or sections
- `Book` stores title, author, ISBN, description, copies, category, cover image, and timestamps
- `Borrowing` stores who borrowed a book, when it was borrowed, when it is due, and whether it was returned
- `Wishlist` stores the books saved by each user

Views:

- `home` shows recent books with cover images
- `BookListView` lists books with search, category filter, and availability filter
- `BookDetailView` shows book details, recent borrowings, related books, and wishlist state
- `borrow_book` creates a borrowing record and reduces available copies
- `toggle_wishlist` adds or removes a book from the user wishlist
- `reserve_book` creates a reservation-style response and reduces available copies when possible
- `wishlist_view` shows saved books for the logged-in user
- `my_borrowings` shows borrowing history for the logged-in user
- `contact` renders the contact page

#### 3. Accounts App

The `accounts` app handles authentication.

Forms:

- `CustomUserCreationForm` extends Django's built-in user creation form and adds a name field

Views:

- `RegisterView` creates a new user and logs them in after successful signup
- `UserLoginView` handles user login
- `UserLogoutView` logs the user out and shows a success message

## How the Code Flow Works

### Public Browsing Flow

1. A user visits `/` and the request is routed to `home` in `book/library/views.py`.
2. `home` queries `Book` objects that have cover images and sends them to `home.html`.
3. The template renders featured book cards using Bootstrap and links each card to the detail page.

### Book List and Search Flow

1. The user visits `/books/`.
2. `BookListView.get_queryset()` builds the query.
3. If a search term is present, the query filters by title or author.
4. If category or availability filters are selected, the queryset is narrowed further.
5. The view sends paginated results and category options to `book_list.html`.

### Book Detail Flow

1. The user opens `/books/<id>/`.
2. `BookDetailView` loads the selected `Book` object.
3. The view adds related books, the latest borrowings, and wishlist status to the template context.
4. `book_detail.html` renders the book information and action buttons.

### Borrow Flow

1. A logged-in user clicks Borrow.
2. The request goes to `borrow_book`.
3. The view checks that at least one copy is available.
4. A `Borrowing` record is created with a due date 14 days ahead.
5. The book's `available_copies` value is reduced and the user is redirected back to the detail page with a success message.

### Wishlist Flow

1. A logged-in user toggles the wishlist action.
2. `toggle_wishlist` checks whether the book already exists in the user's wishlist.
3. If it exists, the record is deleted; otherwise a new one is created.
4. The response is returned as JSON so the front end can update the button state without a full page refresh.

### Reservation Flow

1. A logged-in user sends a POST request to reserve a book.
2. `reserve_book` checks availability.
3. If copies exist, it creates a borrowing-style record and decreases inventory.
4. If no copies exist, the view still returns a response indicating the book was added to the reserve waitlist.

### Authentication Flow

1. `/accounts/register/` opens the signup form.
2. `CustomUserCreationForm` validates the new account data.
3. `RegisterView` saves the user and logs them in immediately.
4. `/accounts/login/` uses Django's login view wrapper.
5. `/accounts/logout/` signs the user out and redirects back to the login page.

## URL Structure

- `/` home page
- `/books/` book list and search
- `/books/<id>/` book detail
- `/books/<id>/borrow/` borrow a book
- `/books/<id>/wishlist/` toggle wishlist status
- `/books/<id>/reserve/` reserve a book
- `/wishlist/` saved books
- `/my-borrowings/` borrowing history
- `/contact/` contact page
- `/accounts/login/` login
- `/accounts/register/` registration
- `/accounts/logout/` logout

## Templates And UI

The UI is built with Django templates under `book/templates/`.

- `library/base.html` provides the shared layout, navigation, search bar, and message area
- `library/home.html` shows featured books
- `library/book_list.html` shows filters, search, and pagination
- `library/book_detail.html` shows the full book detail view and action buttons
- `accounts/login.html` and `accounts/register.html` provide custom authentication pages

The templates use Bootstrap 5 for layout and responsive behavior, with Font Awesome icons and custom CSS for a more polished look.

## Setup And Run

1. Create and activate a virtual environment.
2. Install the dependencies used by the project, including Django and Pillow.
3. Run database migrations.
4. Start the development server from the `book/` directory.

Example commands:

```bash
python manage.py migrate
python manage.py runserver
```

## Notes

- Uploaded book cover images are stored in `book/media/books/`.
- The app uses SQLite for local development.
- Authentication and book actions that modify data require a logged-in user.
