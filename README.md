# Django Task Manager

## Overview

This repository contains the backend for a Task Manager application built with Django.

## Setup and Installation

1. **Clone the Repository**

    ```bash
    git clone https://github.com/ShuhaibMuhammed175/task_manager_server-side.git
    cd task_manager
    ```

2. **Create and Activate a Virtual Environment**

    **On Windows:**

    ```bash
    python -m venv env
    env\Scripts\activate
    ```

    **On macOS/Linux:**

    ```bash
    python3 -m venv env
    source env/bin/activate
    ```
3. **Database Configuration**

    ```bash
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': os.getenv('DB_NAME'),
            'USER': os.getenv('DB_USER'),
            'PASSWORD': os.getenv('DB_PASSWORD'),
            'HOST': os.getenv('DB_HOST'),
            'PORT': os.getenv('DB_PORT'),
        }
    }
    ```

    
4**Create an `.env` File**

    In the root of your project directory, create a file named `.env`. Add the following environment variables to configure your database and Django settings:

    ```bash
    DB_NAME=your_db_name
    DB_USER=your_db_user
    DB_PASSWORD=your_db_password
    DB_HOST=localhost
    DB_PORT=5432
    ```

    Make sure to replace `your_db_name`, `your_db_user`, and `your_db_password` with your actual database credentials. You can generate a secret key using Django's `get_random_secret_key()` method.

5**Install Requirements**

    ```bash
    pip install -r requirements.txt
    ```

6**Apply Migrations**

    ```bash
    python manage.py migrate
    ```

7**Run the Development Server**

    ```bash
    python manage.py runserver
    ```

    The application will be available at `http://127.0.0.1:8000/`.

## Usage

Once the server is running, you can use the following endpoints:

- **List Tasks:** `GET /api/tasks/`
- **Create Task:** `POST /api/tasks/`
- **View Task:** `GET /api/tasks/{id}/`
- **Update Task:** `PUT /api/tasks/{id}/update/`
- **Delete Task:** `DELETE /api/tasks/{id}/delete/`
- **Filter Tasks:** `GET /api/tasks/filter/`

## User Management

The following endpoints are available for user management:

- **Obtain Token:** `POST /api/token/`
  - Use this endpoint to obtain an access token and a refresh token upon successful login.
- **Refresh Token:** `POST /api/token/refresh/`
  - Use this endpoint to refresh the access token using the refresh token. Note: Once a refresh token is used, it will be blacklisted for security purposes and cannot be used again.
- **Register User:** `POST /api/register/`
  - Use this endpoint to register a new user.



