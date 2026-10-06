# Module 5 – Python Application Development

A student-built REST API using **Flask + SQLite + Pydantic**. This project covers the Module 5 requirements: web framework fundamentals, routing and HTTP methods, database integration, SQL CRUD operations, authentication, schema validation, endpoint testing, and API documentation.

## What this project demonstrates

- Flask application and routing
- RESTful API endpoints
- GET, POST, PUT, PATCH and DELETE methods
- SQLite database with SQL CRUD operations
- Bearer-token authentication
- Pydantic request/schema validation
- JSON error handling
- Automated API tests with pytest
- Health check endpoint
- Postman collection for manual API testing
- Structured project layout and documentation

## Project structure

```text
module5-python-rest-api/
├── app/
│   ├── __init__.py
│   ├── config.py
│   ├── db.py
│   ├── auth.py
│   ├── schemas.py
│   └── routes.py
├── tests/
│   └── test_api.py
├── docs/
│   ├── API_DOCUMENTATION.md
│   └── LEARNING_NOTES.md
├── postman/
│   └── module5-api.postman_collection.json
├── run.py
├── requirements.txt
├── .env.example
├── .gitignore
├── LICENSE
└── README.md
```

## Setup

Python 3.10+ is recommended.

```bash
python -m venv .venv
```

Windows:
```bash
.venv\Scripts\activate
```

macOS/Linux:
```bash
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

## Run the API

```bash
python run.py
```

The API starts at `http://127.0.0.1:5000`.

Health check: `GET /api/health`

## Authentication

Demo credentials:

```text
username: student
password: module5
```

Login:

```http
POST /api/auth/login
Content-Type: application/json

{
  "username": "student",
  "password": "module5"
}
```

Use the returned token:

```http
Authorization: Bearer <token>
```

> This is an educational authentication implementation. Production systems should use hashed passwords, a persistent user table, HTTPS, secure secret management, token expiry, and stronger authentication.

## Main API endpoints

| Method | Endpoint | Auth | Purpose |
|---|---|---|---|
| GET | `/api/health` | No | API health check |
| POST | `/api/auth/login` | No | Login and receive token |
| GET | `/api/tasks` | Yes | List tasks |
| GET | `/api/tasks/<id>` | Yes | Get one task |
| POST | `/api/tasks` | Yes | Create task |
| PUT | `/api/tasks/<id>` | Yes | Replace task |
| PATCH | `/api/tasks/<id>` | Yes | Partially update task |
| DELETE | `/api/tasks/<id>` | Yes | Delete task |

## Example create request

```json
{
  "title": "Finish Module 5",
  "description": "Complete Flask REST API project",
  "status": "pending",
  "priority": 2
}
```

## Run tests

```bash
pytest -q
```

The tests cover authentication, validation, CRUD operations, protected routes, 404 handling, and the health check.

## Learning notes

See `docs/LEARNING_NOTES.md`.

## API documentation

See `docs/API_DOCUMENTATION.md`.

## Manual testing

Import `postman/module5-api.postman_collection.json` into Postman after starting the server.

## Academic note

This project is intentionally understandable rather than over-engineered. The goal is to demonstrate Module 5 fundamentals clearly while keeping the code readable for a student learning backend development.
