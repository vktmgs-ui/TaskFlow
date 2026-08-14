# 🚀 TaskFlow

AI-powered task management backend built with **FastAPI, SQLite, SQLAlchemy, Pydantic and Google Gemini API**.

TaskFlow helps users create, manage, search and organize tasks with an AI-powered Quick Add feature.

---

## ✨ Features

- ✅ Create and manage tasks
- ✅ Project-based task management
- ✅ Search tasks by title
- ✅ Sort tasks by priority and due date
- ✅ AI-powered Quick Add task parser
- ✅ Automatic priority detection
- ✅ Due-date hint extraction
- ✅ SQLite database
- ✅ Pydantic validation
- ✅ REST API with FastAPI
- ✅ Insertion Sort implementation
- ✅ Linear Search implementation
- ✅ Binary Search implementation
- ✅ Automated API and algorithm tests
- ✅ GitHub Actions CI

---

## 🛠️ Tech Stack

- Python
- FastAPI
- SQLAlchemy
- Pydantic
- SQLite
- Google Gemini API
- Pytest
- Uvicorn
- GitHub Actions

---

## 📁 Project Structure

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
├── .gitignore
│
├── tests/
│   ├── test_api.py
│   └── test_algorithms.py
│
└── .github/
    └── workflows/
        └── ci.yml

## 📸 API Demo

### Swagger API Documentation

TaskFlow provides interactive API documentation using FastAPI Swagger UI.

### AI Quick Add

The Quick Add API converts a natural-language task description into a structured task.

Example:

```json
{
  "description": "Prepare presentation tomorrow, high priority",
  "project_id": 1
}

{
  "id": 3,
  "due_date": "tomorrow",
  "title": "Prepare presentation , high priority",
  "priority": "medium",
  "project_id": 1
}