# FastAPI Practice Project

This is a simple FastAPI project that demonstrates a user management and authentication system.

## Features

- User registration
- Token-based authentication (JWT)
- User CRUD operations
- OpenAPI (Swagger UI) and ReDoc documentation

## Project Structure

```
/
├── app/
│   ├── __init__.py
│   ├── crud/
│   ├── database.py
│   ├── main.py
│   ├── models/
│   ├── routers/
│   ├── schemas/
│   └── security.py
├── requirements.txt
└── .env
```

## Getting Started

### Prerequisites

- Python 3.8+
- An active virtual environment

### Installation & Setup

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/yuemj8665/FastAPI_Practice3.git
    cd FastAPI_Practice3
    ```

2.  **Create and activate a virtual environment:**
    ```bash
    # For Windows
    python -m venv .venv
    .venv\Scripts\activate

    # For macOS/Linux
    python3 -m venv .venv
    source .venv/bin/activate
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Configure environment variables:**

    Create a `.env` file in the root directory and add the following variables.

    ```env
    DATABASE_URL="sqlite:///./sql_app.db"
    SECRET_KEY="<your_super_secret_key>"
    ALGORITHM="HS256"
    ```
    *Replace `<your_super_secret_key>` with a strong, randomly generated secret key.* You can generate one using `openssl rand -hex 32`.

### Running the Application

Run the development server using `uvicorn`:

```bash
uvicorn app.main:app --reload
```

The application will be available at `http://127.0.0.1:8000`.

## API Documentation

Once the server is running, you can access the interactive API documentation at:

-   **Swagger UI:** `http://127.0.0.1:8000/docs`
-   **ReDoc:** `http://127.0.0.1:8000/redoc`

## API Endpoints

### Authentication (`/auth`)

-   `POST /auth/token`: Login and receive a JWT access token.

### Users (`/users`)

-   `POST /users/`: Create a new user.
-   `GET /users/all`: Get a list of all users.
-   `GET /users/me/`: Get the details of the currently authenticated user.
-   `GET /users/{user_id}`: Get details of a specific user by ID.
-   `DELETE /users/{user_id}`: Delete a specific user by ID.
