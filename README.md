
# Django Snippets Application

This repository contains a Django-based web application that allows users to create and manage code snippets in various programming languages. Snippets can be either public (visible to all users) or private (visible only to the creator).

## Features

- **User Authentication**:

  - Login and Logout functionality.
  - User creation through the Django admin panel.
- **Snippets Management**:

  - CRUD (Create, Read, Update, Delete) operations for code snippets.
  - Public and private visibility for snippets.
  - Syntax highlighting for snippets using [Pygments](https://pygments.org).
- **Programming Languages Management**:

  - CRUD operations for programming languages via the Django admin panel.

## Technologies Used

### Backend

- Python 3.11
- Django 5.1.2
- SQLite (default database)
- Pygments for syntax highlighting

### Frontend

- Bootstrap 4 ([Documentation](https://getbootstrap.com))

## Installation and Setup

### Prerequisites

- Python 3.11 installed on your system.
- A virtual environment tool (e.g., `venv` or `virtualenv`).
- Git (optional, for cloning the repository).

### Steps

1. **Clone the repository**:

   ```bash
   git clone <repository_url>
   cd snippets_test
   ```
2. **Set up a virtual environment**:

   ```bash
   python3 -m venv env
   source env/bin/activate  # On Windows, use `env\Scripts\activate`
   ```
3. **Install dependencies**:

   ```bash
   pip install -r requirements.txt
   ```
4. **Apply migrations**:

   ```bash
   python manage.py migrate
   ```
5. **Create a superuser** (for accessing the admin panel):

   ```bash
   python manage.py createsuperuser
   ```
6. **Run the development server**:

   ```bash
   python manage.py runserver
   ```
7. **Access the application**:

   - Open a browser and navigate to `http://127.0.0.1:8000`.
   - Admin panel is available at `http://127.0.0.1:8000/admin`.

## Usage

1. Log in using the superuser account or a registered user account.
2. Create programming languages through the Django admin panel.
3. Create snippets using the provided interface, specifying the language and visibility.
4. View snippets in the list view, with public snippets accessible to non-registered users.
5. Use the detail view to see syntax-highlighted code.

## Folder Structure

- **`django_snippets/`**: Project settings and configuration.
- **`snippets/`**: Main application containing models, views, and templates for snippets.
- **`static/`**: Static files (CSS, JS, images).
- **`templates/`**: HTML templates for the application.
- **`db.sqlite3`**: Default SQLite database file.
- **`requirements.txt`**: Python dependencies.

## Contribution

Feel free to fork the repository and submit pull requests for improvements or bug fixes.

## License

This project is provided for educational and testing purposes.
