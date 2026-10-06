from functools import wraps

from flask import Blueprint, jsonify, request

from .auth import is_valid_token, login
from .db import get_db
from .schemas import LoginRequest, TaskCreate, TaskUpdate, validate

api = Blueprint("api", __name__)


def require_auth(view):
    @wraps(view)
    def wrapper(*args, **kwargs):
        header = request.headers.get("Authorization", "")
        if not header.startswith("Bearer "):
            return jsonify({"error": "Missing Bearer token"}), 401

        token = header.removeprefix("Bearer ").strip()
        if not is_valid_token(token):
            return jsonify({"error": "Invalid token"}), 401

        return view(*args, **kwargs)

    return wrapper


def row_to_dict(row):
    return dict(row)


@api.get("/health")
def health():
    return jsonify({"status": "ok", "service": "module5-python-rest-api"})


@api.post("/auth/login")
def auth_login():
    payload, errors = validate(LoginRequest, request.get_json(silent=True) or {})
    if errors:
        return jsonify({"error": "Invalid request", "details": errors}), 400

    token = login(payload.username, payload.password)
    if not token:
        return jsonify({"error": "Invalid username or password"}), 401

    return jsonify({"token": token, "token_type": "Bearer"})


@api.get("/tasks")
@require_auth
def list_tasks():
    rows = get_db().execute(
        "SELECT id, title, description, status, priority, created_at "
        "FROM tasks ORDER BY id DESC"
    ).fetchall()
    return jsonify({"items": [row_to_dict(row) for row in rows]})


@api.get("/tasks/<int:task_id>")
@require_auth
def get_task(task_id):
    row = get_db().execute(
        "SELECT id, title, description, status, priority, created_at "
        "FROM tasks WHERE id = ?",
        (task_id,),
    ).fetchone()

    if row is None:
        return jsonify({"error": "Task not found"}), 404

    return jsonify(row_to_dict(row))


@api.post("/tasks")
@require_auth
def create_task():
    payload, errors = validate(TaskCreate, request.get_json(silent=True) or {})
    if errors:
        return jsonify({"error": "Validation failed", "details": errors}), 400

    db = get_db()
    cursor = db.execute(
        "INSERT INTO tasks (title, description, status, priority) VALUES (?, ?, ?, ?)",
        (payload.title, payload.description, payload.status, payload.priority),
    )
    db.commit()

    row = db.execute(
        "SELECT id, title, description, status, priority, created_at "
        "FROM tasks WHERE id = ?",
        (cursor.lastrowid,),
    ).fetchone()

    return jsonify(row_to_dict(row)), 201


@api.put("/tasks/<int:task_id>")
@require_auth
def replace_task(task_id):
    payload, errors = validate(TaskCreate, request.get_json(silent=True) or {})
    if errors:
        return jsonify({"error": "Validation failed", "details": errors}), 400

    db = get_db()
    existing = db.execute("SELECT id FROM tasks WHERE id = ?", (task_id,)).fetchone()
    if existing is None:
        return jsonify({"error": "Task not found"}), 404

    db.execute(
        "UPDATE tasks SET title=?, description=?, status=?, priority=? WHERE id=?",
        (payload.title, payload.description, payload.status, payload.priority, task_id),
    )
    db.commit()

    row = db.execute(
        "SELECT id, title, description, status, priority, created_at "
        "FROM tasks WHERE id = ?",
        (task_id,),
    ).fetchone()

    return jsonify(row_to_dict(row))


@api.patch("/tasks/<int:task_id>")
@require_auth
def update_task(task_id):
    payload, errors = validate(TaskUpdate, request.get_json(silent=True) or {})
    if errors:
        return jsonify({"error": "Validation failed", "details": errors}), 400

    db = get_db()
    existing = db.execute(
        "SELECT id, title, description, status, priority FROM tasks WHERE id = ?",
        (task_id,),
    ).fetchone()

    if existing is None:
        return jsonify({"error": "Task not found"}), 404

    current = dict(existing)
    current.update(payload.model_dump(exclude_none=True))

    db.execute(
        "UPDATE tasks SET title=?, description=?, status=?, priority=? WHERE id=?",
        (
            current["title"],
            current["description"],
            current["status"],
            current["priority"],
            task_id,
        ),
    )
    db.commit()

    row = db.execute(
        "SELECT id, title, description, status, priority, created_at "
        "FROM tasks WHERE id = ?",
        (task_id,),
    ).fetchone()

    return jsonify(row_to_dict(row))


@api.delete("/tasks/<int:task_id>")
@require_auth
def delete_task(task_id):
    db = get_db()
    cursor = db.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
    db.commit()

    if cursor.rowcount == 0:
        return jsonify({"error": "Task not found"}), 404

    return jsonify({"message": "Task deleted", "id": task_id})
