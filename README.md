# Finance App — Virtusa

A web-based personal finance management application built with **Flask** and **MySQL**. It allows users to track their expenses by category, and generate monthly and yearly spending reports through an intuitive browser interface.

---

## Table of Contents

- [Features](#features)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Database Models](#database-models)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
  - [Environment Variables](#environment-variables)
  - [Running the App](#running-the-app)
- [API Reference](#api-reference)
  - [Authentication](#authentication)
  - [Expenses](#expenses)
  - [Categories](#categories)
  - [Reports](#reports)
- [Default Categories](#default-categories)
- [Testing](#testing)
- [AI Disclaimer](#ai-disclaimer)

---

## Features

- **User Authentication** — Register, log in, and log out securely. Passwords are hashed using Werkzeug's `generate_password_hash`.
- **Expense Tracking** — Add and delete personal expense entries with an amount, date, description, and category.
- **Category Management** — Create and delete custom spending categories. New accounts come pre-loaded with six default categories.
- **Reporting** — Generate spending summaries broken down by month and year, both overall and per category.
- **Session-based Security** — Protected routes redirect unauthenticated users to the login page.

---

## Tech Stack

| Layer | Technology |
|---|---|
| Language | Python 3 |
| Web Framework | Flask |
| ORM | Flask-SQLAlchemy |
| Database | MySQL (via PyMySQL driver) |
| Templating | Jinja2 |
| Password Hashing | Werkzeug Security |
| Configuration | python-dotenv |

---

## Project Structure

```
finance-app-virtusa/
├── run.py                   # Application entry point
├── app/
│   ├── __init__.py          # App factory (create_app)
│   ├── extensions.py        # SQLAlchemy instance
│   ├── models.py            # Database models (User, Category, Expense)
│   ├── routes/
│   │   ├── __init__.py      # Blueprint registration
│   │   ├── auth.py          # Login, signup, logout routes
│   │   ├── expense.py       # Expense CRUD routes
│   │   ├── category.py      # Category CRUD routes
│   │   ├── report.py        # Report generation routes
│   │   └── main.py          # Home page route
│   ├── services/
│   │   ├── auth_service.py      # Login/signup business logic
│   │   ├── expense_service.py   # Expense business logic
│   │   ├── category_service.py  # Category business logic
│   │   └── report_service.py    # Report aggregation queries
│   ├── utils/
│   │   └── decorators.py    # login_required decorator
│   ├── templates/           # Jinja2 HTML templates
│   │   ├── base.html
│   │   ├── home.html
│   │   ├── login.html
│   │   ├── signup.html
│   │   ├── expense.html
│   │   ├── category.html
│   │   └── report.html
│   └── static/              # CSS and JavaScript assets
│       ├── css/
│       └── js/
└── test_login.py            # Manual login endpoint test script
```

---

## Database Models

### `User` (`users` table)
| Column | Type | Notes |
|---|---|---|
| `user_id` | BigInteger | Primary key, auto-increment |
| `user_name` | String(255) | Unique |
| `email` | String(255) | Unique |
| `password` | String(255) | Hashed |
| `created_at` | DateTime | Server default: now() |

### `Category` (`category` table)
| Column | Type | Notes |
|---|---|---|
| `category_id` | BigInteger | Primary key, auto-increment |
| `user_id` | BigInteger | FK → `users.user_id` |
| `name` | String(255) | |
| `date_added` | Date | Server default: current date |

### `Expense` (`transaction` table)
| Column | Type | Notes |
|---|---|---|
| `transaction_id` | BigInteger | Primary key, auto-increment |
| `user_id` | BigInteger | FK → `users.user_id` |
| `category_id` | BigInteger | FK → `category.category_id` |
| `amount` | Float | Must be 0 – 999,999,999 |
| `date` | Date | Server default: current date |
| `description` | String(255) | Optional |

---

## Getting Started

### Prerequisites

- Python 3.9+
- MySQL server running locally (or a remote instance)
- `pip` package manager

### Installation

```bash
# Clone the repository
git clone https://github.com/blitz-pixel/finance-app-virtusa.git
cd finance-app-virtusa

# Create and activate a virtual environment
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate

# Install dependencies
pip install flask flask-sqlalchemy pymysql python-dotenv werkzeug
```

### Environment Variables

Create a `.env` file in the project root (it is listed in `.gitignore` and will not be committed):

```env
DATABASE_URI=mysql+pymysql://<user>:<password>@<host>/<database>
SECRET_KEY=your-very-secret-key
FLASK_ENV=development
```

| Variable | Required | Description |
|---|---|---|
| `DATABASE_URI` | Yes (in development) | SQLAlchemy connection string for MySQL |
| `SECRET_KEY` | Yes | Flask session secret key |
| `FLASK_ENV` | No | Set to `development` to bypass the production default DB URI |

> **Note:** When `FLASK_ENV` is `production` and `DATABASE_URI` is not set, the app falls back to `mysql+pymysql://root:1234@localhost/financeappdb`.

### Running the App

```bash
python run.py
```

The application starts in debug mode and is accessible at `http://localhost:5000`.

---

## API Reference

All POST/DELETE endpoints accept and return JSON. Routes protected by `@login_required` redirect unauthenticated requests to `/login`.

### Authentication

#### `GET /`
Renders the home page.

---

#### `GET /login`
Renders the login page.

#### `POST /login`
Log in an existing user.

**Request body:**
```json
{
  "username": "john_doe",
  "password": "secret"
}
```

**Responses:**

| Status | Body |
|---|---|
| `200` | `{"message": "Login successful"}` |
| `400` | `{"message": "Username and password are required"}` |
| `401` | `{"message": "Invalid username or password"}` |
| `500` | `{"message": "An error occurred"}` |

> Accepts either `username` or `email` in the `username` field.

---

#### `GET /signup`
Renders the signup page.

#### `POST /signup`
Register a new user.

**Request body:**
```json
{
  "username": "john_doe",
  "email": "john@example.com",
  "password": "secret"
}
```

**Responses:**

| Status | Body |
|---|---|
| `200` | `{"message": "User registered successfully"}` |
| `400` | `{"message": "Email already exists"}` |
| `400` | `{"message": "Username already exists"}` |
| `500` | `{"message": "An error occurred"}` |

> On successful signup, six default categories are automatically created for the new user.

---

#### `GET /logout`
Clears the session and redirects to `/login`.

---

### Expenses

All expense routes require an active session (`@login_required`).

#### `GET /expense`
Renders the expense page with the user's existing expenses and categories.

#### `POST /expense`
Add a new expense.

**Request body:**
```json
{
  "category": "Housing",
  "amount": 1200.00,
  "date": "2024-06-15",
  "description": "Monthly rent"
}
```

**Responses:**

| Status | Body |
|---|---|
| `200` | `{"message": "Expense added successfully", "date": "...", "transaction_id": 42}` |
| `400` | `{"message": "Amount must be a valid number"}` |
| `400` | `{"message": "Amount cannot be negative"}` |
| `400` | `{"message": "Amount exceeds maximum limit"}` |
| `404` | `{"message": "Category not found"}` |
| `500` | `{"message": "An error occurred"}` |

#### `DELETE /expense?expense_id=<id>`
Delete an expense by its transaction ID.

**Responses:**

| Status | Body |
|---|---|
| `200` | `{"message": "Expense deleted successfully"}` |
| `404` | `{"message": "Expense not found"}` |
| `500` | `{"message": "An error occurred"}` |

---

### Categories

All category routes require an active session (`@login_required`).

#### `GET /category`
Renders the category management page.

#### `POST /category`
Add a new category.

**Request body:**
```json
{
  "name": "Groceries",
  "date": "2024-06-01"
}
```

**Responses:**

| Status | Body |
|---|---|
| `200` | `{"message": "...", "date": "...", "category_id": 7}` |
| `400` | `{"message": "Invalid JSON data"}` |
| `500` | `{"message": "An error occurred"}` |

#### `DELETE /category?category_id=<id>`
Delete a category by its ID.

**Responses:**

| Status | Body |
|---|---|
| `200` | `{"message": "..."}` |
| `400` | `{"message": "category_id is required"}` |
| `500` | `{"message": "An error occurred"}` |

---

### Reports

Requires an active session (`@login_required`).

#### `GET /report`
Renders the report page populated with the user's categories.

#### `POST /report`
Generate spending summaries for the logged-in user.

**Response (200):**
```json
{
  "message": "Report generated successfully",
  "monthly_totals": [
    { "year": 2024, "month": 6, "totalAmount": 2500.00 }
  ],
  "yearly_totals": [
    { "year": 2024, "totalAmount": 15000.00 }
  ],
  "monthly_category_totals": [
    { "category_name": "Housing", "year": 2024, "month": 6, "totalAmount": 1200.00 }
  ],
  "yearly_category_totals": [
    { "category_name": "Housing", "year": 2024, "totalAmount": 7200.00 }
  ]
}
```

---

## Default Categories

Every newly registered user is automatically assigned the following six spending categories:

1. Housing
2. Entertainment
3. Education
4. Transportation
5. Gifts & Donations
6. Miscellaneous

Additional custom categories can be added or removed at any time from the category management page.

---

## Testing

A manual test script for the login endpoint is included:

```bash
# Ensure the app is running on localhost:5000 first
python test_login.py
```

The script sends a `POST /login` request with sample credentials and prints the HTTP status code, headers, and response body to the console.

---

## AI Disclaimer

> This README was created using AI.
