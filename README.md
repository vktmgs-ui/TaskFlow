# TaskFlow

TaskFlow is a FastAPI-based task management backend with AI-powered Quick Add, task search, sorting, and algorithm utilities.

## Features

- Create and manage tasks
- Project-based task management
- Search tasks by title
- Sort tasks by priority and due date
- AI-powered Quick Add task parser
- Priority detection
- Due-date hint extraction
- Insertion Sort implementation
- Linear Search implementation
- Binary Search implementation
- SQLite database
- Pydantic validation
- Automated API and algorithm tests

## Tech Stack

- Python
- FastAPI
- SQLAlchemy
- Pydantic
- SQLite
- Google Gemini API
- Pytest
- Uvicorn

## Project Structure

```text
TaskFlow/
├── backend/
│   ├── main.py
│   ├── crud.py
│   ├── database.py
│   ├── models.py
│   ├── schemas.py
│   ├── ai_service.py
│   ├── quick_add.py
│   ├── algorithms.py
│   ├── requirements.txt
│   ├── .gitignore
│   └── tests/
│       ├── test_api.py
│       └── test_algorithms.py
│
└── README.md