# API Documentation

Base URL:

```text
http://127.0.0.1:5000/api
```

## Health

`GET /health`

No authentication required.

## Login

`POST /auth/login`

```json
{
  "username": "student",
  "password": "module5"
}
```

Returns a Bearer token.

## List tasks

`GET /tasks`

Requires:

```text
Authorization: Bearer <token>
```

## Get task

`GET /tasks/<id>`

Returns one task or 404.

## Create task

`POST /tasks`

```json
{
  "title": "Finish Module 5",
  "description": "Complete Flask project",
  "status": "pending",
  "priority": 2
}
```

Validation:

- title: 1–120 characters
- description: maximum 500 characters
- status: `pending`, `in_progress`, or `completed`
- priority: integer 1–5

## Replace task

`PUT /tasks/<id>`

Requires a complete valid task object.

## Partial update

`PATCH /tasks/<id>`

Example:

```json
{
  "status": "completed"
}
```

## Delete task

`DELETE /tasks/<id>`

Response:

```json
{
  "message": "Task deleted",
  "id": 1
}
```

## Status codes

| Code | Meaning |
|---|---|
| 200 | Successful request |
| 201 | Resource created |
| 400 | Invalid request/validation |
| 401 | Authentication required/failed |
| 404 | Resource not found |
| 405 | Method not allowed |
