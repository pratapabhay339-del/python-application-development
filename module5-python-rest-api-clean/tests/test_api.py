import pytest

from app import create_app


@pytest.fixture()
def client(tmp_path):
    app = create_app(
        {
            "TESTING": True,
            "DATABASE_PATH": str(tmp_path / "test.db"),
            "SECRET_KEY": "test-secret",
        }
    )
    return app.test_client()


def get_token(client):
    response = client.post(
        "/api/auth/login",
        json={"username": "student", "password": "module5"},
    )
    assert response.status_code == 200
    return response.get_json()["token"]


def auth_headers(token):
    return {"Authorization": f"Bearer {token}"}


def test_health(client):
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.get_json()["status"] == "ok"


def test_protected_route_requires_auth(client):
    response = client.get("/api/tasks")
    assert response.status_code == 401


def test_invalid_login(client):
    response = client.post(
        "/api/auth/login",
        json={"username": "student", "password": "wrong"},
    )
    assert response.status_code == 401


def test_task_crud(client):
    token = get_token(client)
    headers = auth_headers(token)

    create = client.post(
        "/api/tasks",
        headers=headers,
        json={
            "title": "Learn Flask",
            "description": "Build a REST API",
            "status": "pending",
            "priority": 2,
        },
    )
    assert create.status_code == 201
    task_id = create.get_json()["id"]

    get_one = client.get(f"/api/tasks/{task_id}", headers=headers)
    assert get_one.status_code == 200
    assert get_one.get_json()["title"] == "Learn Flask"

    patch = client.patch(
        f"/api/tasks/{task_id}",
        headers=headers,
        json={"status": "completed"},
    )
    assert patch.status_code == 200
    assert patch.get_json()["status"] == "completed"

    listing = client.get("/api/tasks", headers=headers)
    assert listing.status_code == 200
    assert len(listing.get_json()["items"]) == 1

    delete = client.delete(f"/api/tasks/{task_id}", headers=headers)
    assert delete.status_code == 200

    missing = client.get(f"/api/tasks/{task_id}", headers=headers)
    assert missing.status_code == 404


def test_validation(client):
    token = get_token(client)
    response = client.post(
        "/api/tasks",
        headers=auth_headers(token),
        json={"title": "", "priority": 10},
    )
    assert response.status_code == 400
