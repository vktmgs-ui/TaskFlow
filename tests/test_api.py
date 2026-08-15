import sys
from pathlib import Path
from uuid import uuid4

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from fastapi.testclient import TestClient
from main import app


client = TestClient(app)


def test_get_tasks():
    response = client.get("/tasks")

    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_quick_add():
    # Create a unique user for every test run
    unique_email = f"ci-test-{uuid4().hex}@taskflow.com"

    user_response = client.post(
        "/users",
        json={
            "name": "CI Test User",
            "email": unique_email
        }
    )

    assert user_response.status_code == 200

    user_id = user_response.json()["id"]

    # Create project for the newly created user
    project_response = client.post(
        "/projects",
        json={
            "name": "Test Project",
            "owner_id": user_id
        }
    )

    assert project_response.status_code == 200

    project_id = project_response.json()["id"]

    # Add task to the project
    response = client.post(
        "/tasks/quick-add",
        json={
            "description": "Prepare presentation tomorrow, high priority",
            "project_id": project_id
        }
    )

    assert response.status_code == 201

    data = response.json()

    assert data["title"] == "Prepare presentation tomorrow"
    assert data["priority"] == "high"
    assert data["due_date"] == "tomorrow"
    assert data["project_id"] == project_id