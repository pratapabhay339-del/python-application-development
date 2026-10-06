# Module 5 Learning Notes – Python Application Development

## 1. Flask fundamentals

Flask is a lightweight Python web framework. A Flask application receives HTTP requests, runs Python functions, and returns HTTP responses.

Important concepts:
- application object
- routes
- request/response
- blueprints
- JSON
- HTTP status codes

## 2. Routing and HTTP methods

REST APIs use URLs for resources and HTTP methods for operations.

- GET `/tasks` → read collection
- GET `/tasks/1` → read one resource
- POST `/tasks` → create
- PUT `/tasks/1` → replace
- PATCH `/tasks/1` → partial update
- DELETE `/tasks/1` → delete

## 3. SQLite and SQL CRUD

SQLite is a file-based relational database.

CRUD means:
- Create → INSERT
- Read → SELECT
- Update → UPDATE
- Delete → DELETE

Parameterized SQL is used to avoid directly inserting user input into SQL strings.

## 4. Authentication

Authentication answers "Who are you?"

This project uses a simple educational Bearer-token flow:
1. Client sends username/password.
2. Server verifies credentials.
3. Server creates a token.
4. Client sends `Authorization: Bearer <token>`.
5. Protected endpoints verify the token.

This is intentionally simplified for learning. Production systems require stronger security.

## 5. Schema validation

Pydantic models define the expected JSON structure and validation rules. Invalid data is rejected before database operations.

## 6. API testing

Pytest and Flask's test client verify:
- health check
- login
- protected routes
- CRUD
- validation
- missing resources

## 7. What I learned

The main lesson was connecting Python, HTTP, authentication, validation and SQL into one working application instead of treating them as isolated topics.

## 8. Possible improvements

- hashed passwords
- JWT with expiry
- user database
- pagination/filtering
- PostgreSQL
- Docker
- deployment
- OpenAPI/Swagger UI
- GitHub Actions CI
