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