from fastapi import FastAPI, Depends, Query, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from quick_add import parse_quick_add
from database import engine, Base, get_db
import models

from schemas import (
    UserCreate,
    ProjectCreate,
    TaskCreate,
    TaskUpdate,
    QuickAddRequest,
    SignupRequest,
    LoginRequest
)

from algorithms import (
    insertion_sort,
    binary_search,
    linear_search
)


Base.metadata.create_all(bind=engine)

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def home():
    return {
        "message": "Welcome to TaskFlow"
    }


@app.get("/test-db")
def test_database(db: Session = Depends(get_db)):
    return {
        "message": "Database connection is working"
    }
@app.post("/auth/signup")
def signup(
    user_data: SignupRequest,
    db: Session = Depends(get_db)
):
    existing_user = (
        db.query(models.User)
        .filter(models.User.email == user_data.email)
        .first()
    )

    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Email already registered"
        )

    new_user = models.User(
        name=user_data.name,
        email=user_data.email,
        password=user_data.password
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {
        "message": "Signup successful",
        "user": {
            "id": new_user.id,
            "name": new_user.name,
            "email": new_user.email
        }
    }
@app.post("/auth/login")
def login(
    user_data: LoginRequest,
    db: Session = Depends(get_db)
):
    user = (
        db.query(models.User)
        .filter(models.User.email == user_data.email)
        .first()
    )

    if not user:
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    if user.password != user_data.password:
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    return {
        "message": "Login successful",
        "user": {
            "id": user.id,
            "name": user.name,
            "email": user.email
        }
    }

@app.post("/users")
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    new_user = models.User(
        name=user.name,
        email=user.email
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

@app.get("/users")
def get_users(db: Session = Depends(get_db)):
    users = db.query(models.User).all()

    return users
@app.post("/projects")
def create_project(
    project: ProjectCreate,
    db: Session = Depends(get_db)
):
    new_project = models.Project(
        name=project.name,
        owner_id=project.owner_id
    )

    db.add(new_project)
    db.commit()
    db.refresh(new_project)

    return new_project
@app.get("/projects")
def get_projects(db: Session = Depends(get_db)):
    projects = db.query(models.Project).all()

    return projects
@app.post("/tasks")
def create_task(
    task: TaskCreate,
    db: Session = Depends(get_db)
):
    new_task = models.Task(
        title=task.title,
        priority=task.priority,
        due_date=task.due_date,
        project_id=task.project_id
    )

    db.add(new_task)
    db.commit()
    db.refresh(new_task)

    return new_task
@app.get("/tasks")
def get_tasks(
    search: str | None = None,
    sort: str | None = None,
    db: Session = Depends(get_db)
):
    query = db.query(models.Task)

    if search:
        query = query.filter(
            models.Task.title.ilike(f"%{search}%")
        )

    tasks = query.all()

    if sort == "priority":
        priority_order = {
            "high": 1,
            "medium": 2,
            "low": 3
        }

        insertion_sort(
            tasks,
            key=lambda task: priority_order.get(str(task.priority).lower(), 99)
        )

    elif sort == "due_date":
        insertion_sort(
            tasks,
            key=lambda task: task.due_date or ""
        )

    return tasks
@app.get("/tasks/{task_id}")
def get_task(task_id: int, db: Session = Depends(get_db)):
    task = db.query(models.Task).filter(
        models.Task.id == task_id
    ).first()

    if task is None:
        return {
            "message": "Task not found"
        }

    return task
@app.put("/tasks/{task_id}")
def update_task(
    task_id: int,
    task_data: TaskUpdate,
    db: Session = Depends(get_db)
):
    task = db.query(models.Task).filter(
        models.Task.id == task_id
    ).first()

    if task is None:
        return {
            "message": "Task not found"
        }

    task.title = task_data.title
    task.priority = task_data.priority
    task.due_date = task_data.due_date
    task.completed = task_data.completed

    db.commit()
    db.refresh(task)

    return task
@app.delete("/tasks/{task_id}")
def delete_task(
    task_id: int,
    db: Session = Depends(get_db)
):
    task = db.query(models.Task).filter(
        models.Task.id == task_id
    ).first()

    if task is None:
        return {
            "message": "Task not found"
        }

    db.delete(task)
    db.commit()

    return {
        "message": "Task deleted successfully"
    }
from sqlalchemy import func
@app.get("/stats")
def get_stats(db: Session = Depends(get_db)):
    results = (
        db.query(
            models.Project.name,
            func.count(models.Task.id).label("task_count")
        )
        .outerjoin(
            models.Task,
            models.Project.id == models.Task.project_id
        )
        .group_by(models.Project.id, models.Project.name)
        .all()
    )

    return [
        {
            "project": project_name,
            "task_count": task_count
        }
        for project_name, task_count in results
    ]

@app.post("/tasks/quick-add", status_code=201)
def quick_add_task(
    data: QuickAddRequest,
    db: Session = Depends(get_db)
):
    project = db.query(models.Project).filter(
        models.Project.id == data.project_id
    ).first()

    if not project:
        raise HTTPException(
            status_code=422,
            detail="Project does not exist"
        )

    parsed = parse_quick_add(data.description)

    task = models.Task(
        title=parsed["title"],
        priority=parsed["priority"],
        due_date=parsed["due_date_hint"],
        project_id=data.project_id
    )

    db.add(task)
    db.commit()
    db.refresh(task)

    return task

@app.get("/tasks/search")
def search_tasks(
    title: str,
    algo: str = "linear",
    db: Session = Depends(get_db)
):
    # Get real tasks from database
    tasks = db.query(models.Task).all()

    # Build an index sorted by title
    indexed_tasks = sorted(
        tasks,
        key=lambda task: task.title.lower()
    )

    # Choose search algorithm
    if algo == "binary":
        result = binary_search(
            indexed_tasks,
            title.lower(),
            key=lambda task: task.title.lower()
        )

    elif algo == "linear":
        result = linear_search(
            indexed_tasks,
            title.lower(),
            key=lambda task: task.title.lower()
        )

    else:
        raise HTTPException(
            status_code=422,
            detail="algo must be binary or linear"
        )

    if result is None:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    return result