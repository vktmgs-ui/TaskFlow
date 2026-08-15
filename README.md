# TaskFlow

TaskFlow is a full-stack task management application built with FastAPI and React. It allows users to securely log in, manage projects and tasks, track progress, search and filter tasks, and use a Quick Add feature for natural-language task creation.

## Features

* User Signup and Login
* Login protection and Logout
* User-specific projects
* Task creation and management
* Complete / Pending task status
* Edit tasks
* Delete tasks
* Search tasks by title
* Priority filtering
* Task sorting
* Dashboard progress percentage
* Quick Add task parser
* Automatic priority detection
* Due-date hint extraction
* SQLite database
* SQLAlchemy ORM
* Pydantic validation
* FastAPI REST API
* React frontend
* Algorithm implementations:

  * Insertion Sort
  * Linear Search
  * Binary Search
* Automated API and algorithm tests
* GitHub Actions CI

## Tech Stack

### Backend

* Python 3.12+
* FastAPI
* SQLAlchemy
* Pydantic
* SQLite
* Uvicorn
* Pytest

### Frontend

* React
* Vite
* React Router
* JavaScript
* CSS

### Development and CI

* Git
* GitHub
* GitHub Actions

## Project Structure

```text
TaskFlow/
│
├── main.py
├── crud.py
├── database.py
├── models.py
├── schemas.py
├── ai_service.py
├── quick_add.py
├── algorithms.py
├── requirements.txt
├── README.md
├── .gitignore
│
├── tests/
│   ├── test_api.py
│   └── test_algorithms.py
│
├── frontend/
│   ├── src/
│   │   ├── App.jsx
│   │   ├── Login.jsx
│   │   ├── Signup.jsx
│   │   ├── main.jsx
│   │   └── ...
│   ├── package.json
│   └── ...
│
└── .github/
    └── workflows/
        └── ci.yml
```

## Backend Setup

Open PowerShell in the TaskFlow project folder.

Create a virtual environment:

```powershell
python -m venv .venv
```

Activate it:

```powershell
.\.venv\Scripts\Activate.ps1
```

Install dependencies:

```powershell
python -m pip install -r requirements.txt
```

Start the FastAPI backend:

```powershell
uvicorn main:app --reload
```

Backend will run at:

```text
http://127.0.0.1:8000
```

## API Documentation

FastAPI provides interactive Swagger documentation at:

```text
http://127.0.0.1:8000/docs
```

Alternative ReDoc documentation:

```text
http://127.0.0.1:8000/redoc
```

## Frontend Setup

Open another PowerShell terminal.

Go to the frontend folder:

```powershell
cd frontend
```

Install frontend dependencies:

```powershell
npm install
```

Start the development server:

```powershell
npm run dev
```

Frontend will normally run at:

```text
http://localhost:5173
```

## Quick Add

TaskFlow supports natural-language task creation through the Quick Add API.

Example request:

```json
{
  "description": "Prepare presentation tomorrow, high priority",
  "project_id": 1
}
```

The parser extracts information such as:

* Task title
* Priority
* Due-date hint

Example response:

```json
{
  "title": "Prepare presentation",
  "priority": "high",
  "project_id": 1,
  "due_date": null,
  "id": 1,
  "completed": false
}
```

## Search and Algorithms

TaskFlow includes implementations of common searching and sorting algorithms.

### Insertion Sort

Used for task sorting, including priority and due-date ordering.

### Linear Search

Searches tasks sequentially.

### Binary Search

Searches an indexed and sorted task collection efficiently.

## Testing

Run all backend tests with:

```powershell
pytest -v
```

Current test suite:

```text
5 passed
```

Tests cover:

* Insertion Sort
* Linear Search
* Binary Search
* Task API
* Quick Add API

## Continuous Integration

TaskFlow uses GitHub Actions for automated testing.

Workflow file:

```text
.github/workflows/ci.yml
```

The CI pipeline:

1. Checks out the repository
2. Sets up Python
3. Installs dependencies
4. Runs the complete pytest test suite

A successful GitHub Actions run confirms that the automated test suite passes.

## Database

TaskFlow uses SQLite with SQLAlchemy.

The database stores application data such as:

* Users
* Projects
* Tasks

## Authentication

TaskFlow provides:

* User registration
* User login
* Login protection
* Logout
* User-specific dashboard access

## Dashboard

The dashboard provides:

* Project selection
* Total task count
* Completed task count
* Pending task count
* Progress percentage
* Search
* Priority filter
* Sorting
* Task actions

## Running the Complete Application

Use two terminals.

### Terminal 1 — Backend

```powershell
cd TaskFlow
.\.venv\Scripts\Activate.ps1
uvicorn main:app --reload
```

### Terminal 2 — Frontend

```powershell
cd TaskFlow\frontend
npm run dev
```

Then open:

```text
http://localhost:5173
```

## Project Status

TaskFlow development and testing are complete.

* Backend working
* Frontend working
* Authentication working
* Dashboard working
* Task management working
* Search/filter/sort working
* Quick Add working
* Automated tests passing
* GitHub Actions CI passing

## Author

TaskFlow Project

Built as a full-stack software development project demonstrating:

* Backend API development
* Frontend development
* Database integration
* Authentication
* Algorithms and data structures
* Automated testing
* Git/GitHub workflow
* Continuous Integration
