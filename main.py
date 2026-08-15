from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy import func

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


# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI()


# --------------------------------------------------
# CORS
# --------------------------------------------------

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


# --------------------------------------------------
# HOME
# --------------------------------------------------

@app.get("/")
def home():
    return {
        "message": "Welcome to TaskFlow"
    }


# --------------------------------------------------
# DATABASE TEST
# --------------------------------------------------

@app.get("/test-db")
def test_database(db: Session = Depends(get_db)):
    return {
        "message": "Database connection is working"
    }


# --------------------------------------------------
# AUTH - SIGNUP
# --------------------------------------------------

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

    # Automatically create a project for new user
    new_project = models.Project(
        name="My Tasks",
        owner_id=new_user.id
    )

    db.add(new_project)
    db.commit()
    db.refresh(new_project)

    return {
        "message": "Signup successful",
        "user": {
            "id": new_user.id,
            "name": new_user.name,
            "email": new_user.email,
            "project_id": new_project.id
        }
    }


# --------------------------------------------------
# AUTH - LOGIN
# --------------------------------------------------

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

    # Find user's project
    project = (
        db.query(models.Project)
        .filter(models.Project.owner_id == user.id)
        .first()
    )

    # If old user has no project, create one
    if project is None:
        project = models.Project(
            name="My Tasks",
            owner_id=user.id
        )

        db.add(project)
        db.commit()
        db.refresh(project)

    return {
        "message": "Login successful",
        "user": {
            "id": user.id,
            "name": user.name,
            "email": user.email,
            "project_id": project.id
        }
    }


# --------------------------------------------------
# USERS
# --------------------------------------------------

@app.post("/users")
def create_user(
    user: UserCreate,
    db: Session = Depends(get_db)
):
    existing_user = (
        db.query(models.User)
        .filter(models.User.email == user.email)
        .first()
    )

    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Email already registered"
        )

    new_user = models.User(
        name=user.name,
        email=user.email,
        password=""
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


@app.get("/users")
def get_users(
    db: Session = Depends(get_db)
):
    users = db.query(models.User).all()

    return [
        {
            "id": user.id,
            "name": user.name,
            "email": user.email
        }
        for user in users
    ]


# --------------------------------------------------
# PROJECTS
# --------------------------------------------------

@app.post("/projects")
def create_project(
    project: ProjectCreate,
    db: Session = Depends(get_db)
):
    user = (
        db.query(models.User)
        .filter(models.User.id == project.owner_id)
        .first()
    )

    if user is None:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    new_project = models.Project(
        name=project.name,
        owner_id=project.owner_id
    )

    db.add(new_project)
    db.commit()
    db.refresh(new_project)

    return new_project


@app.get("/projects")
def get_projects(
    db: Session = Depends(get_db)
):
    projects = db.query(models.Project).all()

    return projects


@app.get("/users/{user_id}/projects")
def get_user_projects(
    user_id: int,
    db: Session = Depends(get_db)
):
    user = (
        db.query(models.User)
        .filter(models.User.id == user_id)
        .first()
    )

    if user is None:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    projects = (
        db.query(models.Project)
        .filter(models.Project.owner_id == user_id)
        .all()
    )

    return projects


# --------------------------------------------------
# TASKS - CREATE
# --------------------------------------------------

@app.post("/tasks")
def create_task(
    task: TaskCreate,
    db: Session = Depends(get_db)
):
    project = (
        db.query(models.Project)
        .filter(models.Project.id == task.project_id)
        .first()
    )

    if project is None:
        raise HTTPException(
            status_code=404,
            detail="Project not found"
        )

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


# --------------------------------------------------
# TASKS - GET
# --------------------------------------------------

@app.get("/tasks")
def get_tasks(
    project_id: int | None = None,
    search: str | None = None,
    sort: str | None = None,
    db: Session = Depends(get_db)
):
    query = db.query(models.Task)

    # Filter by project
    if project_id is not None:
        query = query.filter(
            models.Task.project_id == project_id
        )

    # Search
    if search:
        query = query.filter(
            models.Task.title.ilike(
                f"%{search}%"
            )
        )

    tasks = query.all()

    # Sort by priority
    if sort == "priority":
        priority_order = {
            "high": 1,
            "medium": 2,
            "low": 3
        }

        insertion_sort(
            tasks,
            key=lambda task:
                priority_order.get(
                    str(task.priority).lower(),
                    99
                )
        )

    # Sort by due date
    elif sort == "due_date":
        insertion_sort(
            tasks,
            key=lambda task:
                task.due_date or ""
        )

    # Sort by title
    elif sort == "title":
        insertion_sort(
            tasks,
            key=lambda task:
                task.title.lower()
        )

    return tasks


# --------------------------------------------------
# TASKS - GET SINGLE
# --------------------------------------------------

@app.get("/tasks/{task_id}")
def get_task(
    task_id: int,
    db: Session = Depends(get_db)
):
    task = (
        db.query(models.Task)
        .filter(models.Task.id == task_id)
        .first()
    )

    if task is None:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    return task


# --------------------------------------------------
# TASKS - UPDATE
# --------------------------------------------------

@app.put("/tasks/{task_id}")
def update_task(
    task_id: int,
    task_data: TaskUpdate,
    db: Session = Depends(get_db)
):
    task = (
        db.query(models.Task)
        .filter(models.Task.id == task_id)
        .first()
    )

    if task is None:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    task.title = task_data.title
    task.priority = task_data.priority
    task.due_date = task_data.due_date
    task.completed = task_data.completed

    db.commit()
    db.refresh(task)

    return task


# --------------------------------------------------
# TASKS - DELETE
# --------------------------------------------------

@app.delete("/tasks/{task_id}")
def delete_task(
    task_id: int,
    db: Session = Depends(get_db)
):
    task = (
        db.query(models.Task)
        .filter(models.Task.id == task_id)
        .first()
    )

    if task is None:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    db.delete(task)
    db.commit()

    return {
        "message": "Task deleted successfully"
    }


# --------------------------------------------------
# TASK QUICK ADD
# --------------------------------------------------

@app.post(
    "/tasks/quick-add",
    status_code=201
)
def quick_add_task(
    data: QuickAddRequest,
    db: Session = Depends(get_db)
):
    project = (
        db.query(models.Project)
        .filter(
            models.Project.id == data.project_id
        )
        .first()
    )

    if not project:
        raise HTTPException(
            status_code=422,
            detail="Project does not exist"
        )

    parsed = parse_quick_add(
        data.description
    )

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


# --------------------------------------------------
# TASK SEARCH
# --------------------------------------------------

@app.get("/tasks/search")
def search_tasks(
    title: str,
    algo: str = "linear",
    project_id: int | None = None,
    db: Session = Depends(get_db)
):
    query = db.query(models.Task)

    if project_id is not None:
        query = query.filter(
            models.Task.project_id == project_id
        )

    tasks = query.all()

    indexed_tasks = sorted(
        tasks,
        key=lambda task:
            task.title.lower()
    )

    if algo == "binary":
        result = binary_search(
            indexed_tasks,
            title.lower(),
            key=lambda task:
                task.title.lower()
        )

    elif algo == "linear":
        result = linear_search(
            indexed_tasks,
            title.lower(),
            key=lambda task:
                task.title.lower()
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


# --------------------------------------------------
# STATS
# --------------------------------------------------

@app.get("/stats")
def get_stats(
    project_id: int | None = None,
    db: Session = Depends(get_db)
):
    query = (
        db.query(
            models.Project.name,
            func.count(models.Task.id).label(
                "task_count"
            )
        )
        .outerjoin(
            models.Task,
            models.Project.id ==
            models.Task.project_id
        )
    )

    if project_id is not None:
        query = query.filter(
            models.Project.id == project_id
        )

    results = (
        query
        .group_by(
            models.Project.id,
            models.Project.name
        )
        .all()
    )

    return [
        {
            "project": project_name,
            "task_count": task_count
        }
        for project_name, task_count in results
    ]