import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_get_tasks():
    response = client.get("/tasks")

    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_quick_add():
    project_response = client.post(
        "/projects",
        json={
            "name": "Test Project",
            "owner_id": 1
        }
    )

    assert project_response.status_code == 200

    project_id = project_response.json()["id"]

    response = client.post(
        "/tasks/quick-add",
        json={
            "description": "Prepare presentation tomorrow, high priority",
            "project_id": project_id
        }
    )

    assert response.status_code == 201
