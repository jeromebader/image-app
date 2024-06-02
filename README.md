# Image App

This is a Flask-based web application that allows to handle multiple users to upload, rename, download, and delete images.
Each user has their own account and can manage their images independently. The app is using a database for user- and filemanagement, files are stored locally.

## Features

- User Registration and Login
- Image Upload
- Image Rename
- Image Download
- Image Delete
- User Account Deletion with Image Deletion After a Specified Period
- Data Overview for Admin (List of Users and Images)

## Installation

### Prerequisites

- Python 3.10+
- Flask
- SQLite

### Steps

1. **Clone the repository:**

    ```sh
    git clone https://github.com/jeromebader/image-app.git
    cd image-app
    ```

2. **Create and activate a virtual environment:**

    ```sh
    python3 -m venv env
    source env/bin/activate  # On Windows use `env\Scripts\activate`
    ```

3. **Install the required packages:**

    ```sh
    pip install -r requirements.txt
    ```

4. **Set up the configuration in `__init__.py`:**

    In `app/__init__.py`, configure the `SECRET_KEY` and `SQLALCHEMY_DATABASE_URI`:

    ```python
    app.config['SECRET_KEY'] = 'your_secret_key'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
    app.config['UPLOAD_FOLDER'] = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static/uploads')
    ```

    Please ensure that the folder `'static/uploads'` is created and has sufficient writting and reading rights.

5. **Run the application:**

    ```sh
    flask run
    ```

The application should now be running at `http://127.0.0.1:5000`.

## Docker Deployment

To deploy the application using Docker:

1. **Build the Docker image:**

    ```sh
    docker build -t yourusername/image-app:latest .
    ```

2. **Run the Docker container:**
    ```sh
    docker run -d -p 5000:5000 -v /path/to/uploads:/app/static/uploads -e UPLOAD_FOLDER=/path/to/uploads yourusername/image-app:latest
    ```

    Replace `/path/to/uploads` with the actual path where you want to store the uploaded images. Also replace the username or path accordingly.

## Usage

1. **Register an account:**
   - Go to `http://127.0.0.1:5000/register` and create a new account.

2. **Log in:**
   - Log in with your registered email and password.

3. **Upload Images:**
   - After logging in, you can upload images, rename them, download them, or delete them.

4. **Admin Data Overview:**
   - An authenticated admin user can access the data overview at `http://127.0.0.1:5000/data`.

## Contributing

Feel free to submit issues and enhancement requests.

