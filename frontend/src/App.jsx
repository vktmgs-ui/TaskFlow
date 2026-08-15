import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import "./App.css";

const API_URL = "http://127.0.0.1:8000";

function App() {
  const navigate = useNavigate();

  const [user, setUser] = useState(null);
  const [project, setProject] = useState(null);

  const [showForm, setShowForm] = useState(false);
  const [task, setTask] = useState("");
  const [tasks, setTasks] = useState([]);
  const [editingTask, setEditingTask] = useState(null);

  const [search, setSearch] = useState("");
  const [priorityFilter, setPriorityFilter] = useState("all");
  const [sortBy, setSortBy] = useState("none");

  const [loading, setLoading] = useState(true);

  // --------------------------------------------------
  // Get logged-in user
  // --------------------------------------------------

  useEffect(() => {
    const savedUser = localStorage.getItem("taskflow_user");

    if (!savedUser) {
      navigate("/login");
      return;
    }

    try {
      const parsedUser = JSON.parse(savedUser);

      if (!parsedUser.id) {
        localStorage.removeItem("taskflow_user");
        navigate("/login");
        return;
      }

      setUser(parsedUser);
    } catch (error) {
      console.error("Invalid user data:", error);
      localStorage.removeItem("taskflow_user");
      navigate("/login");
    }
  }, [navigate]);

  // --------------------------------------------------
  // Load user's project
  // --------------------------------------------------

  const loadProject = async (userId) => {
    try {
      const response = await fetch(
        `${API_URL}/users/${userId}/projects`
      );

      if (!response.ok) {
        throw new Error("Failed to load project");
      }

      const data = await response.json();

      if (data.length === 0) {
        throw new Error("No project found");
      }

      const userProject = data[0];

      setProject(userProject);

      return userProject;
    } catch (error) {
      console.error("Error loading project:", error);
      alert("Unable to load your project");
      return null;
    }
  };

  // --------------------------------------------------
  // Load tasks for current project
  // --------------------------------------------------

  const loadTasks = async (projectId) => {
    try {
      const response = await fetch(
        `${API_URL}/tasks?project_id=${projectId}`
      );

      if (!response.ok) {
        throw new Error("Failed to load tasks");
      }

      const data = await response.json();

      setTasks(data);
    } catch (error) {
      console.error("Error loading tasks:", error);
      alert("Unable to load tasks");
    }
  };

  // --------------------------------------------------
  // Initialize Dashboard
  // --------------------------------------------------

  useEffect(() => {
    const initializeDashboard = async () => {
      if (!user) {
        return;
      }

      setLoading(true);

      let currentProject = null;

      // Login response already contains project_id
      if (user.project_id) {
        currentProject = {
          id: user.project_id,
          name: "My Tasks",
          owner_id: user.id,
        };

        setProject(currentProject);
      } else {
        currentProject = await loadProject(user.id);
      }

      if (currentProject) {
        await loadTasks(currentProject.id);
      }

      setLoading(false);
    };

    initializeDashboard();
  }, [user]);

  // --------------------------------------------------
  // Add Task
  // --------------------------------------------------

  const addTask = async () => {
    if (!task.trim()) {
      alert("Please enter a task");
      return;
    }

    if (!project) {
      alert("Project is not available");
      return;
    }

    try {
      const response = await fetch(
        `${API_URL}/tasks/quick-add`,
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            description: task.trim(),
            project_id: project.id,
          }),
        }
      );

      const data = await response.json();

      if (!response.ok) {
        alert(data.detail || "Failed to add task");
        return;
      }

      setTask("");
      setShowForm(false);

      await loadTasks(project.id);

      alert("Task added successfully!");
    } catch (error) {
      console.error("Error adding task:", error);
      alert("Backend server is not running");
    }
  };

  // --------------------------------------------------
  // Complete / Pending
  // --------------------------------------------------

  const toggleComplete = async (item) => {
    try {
      const response = await fetch(
        `${API_URL}/tasks/${item.id}`,
        {
          method: "PUT",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            title: item.title,
            priority: item.priority,
            due_date: item.due_date,
            completed: !item.completed,
          }),
        }
      );

      const data = await response.json();

      if (!response.ok) {
        alert(
          data.detail || "Failed to update task"
        );
        return;
      }

      await loadTasks(project.id);
    } catch (error) {
      console.error("Error updating task:", error);
      alert("Failed to update task");
    }
  };

  // --------------------------------------------------
  // Delete Task
  // --------------------------------------------------

  const deleteTask = async (taskId) => {
    const confirmDelete = window.confirm(
      "Are you sure you want to delete this task?"
    );

    if (!confirmDelete) {
      return;
    }

    try {
      const response = await fetch(
        `${API_URL}/tasks/${taskId}`,
        {
          method: "DELETE",
        }
      );

      const data = await response.json();

      if (!response.ok) {
        alert(
          data.detail || "Failed to delete task"
        );
        return;
      }

      await loadTasks(project.id);

      alert("Task deleted successfully!");
    } catch (error) {
      console.error("Error deleting task:", error);
      alert("Failed to delete task");
    }
  };

  // --------------------------------------------------
  // Start Edit
  // --------------------------------------------------

  const startEdit = (item) => {
    setEditingTask({
      id: item.id,
      title: item.title,
      priority: item.priority,
      due_date: item.due_date || "",
      completed: item.completed,
    });
  };

  // --------------------------------------------------
  // Save Edit
  // --------------------------------------------------

  const saveEdit = async () => {
    if (!editingTask) {
      return;
    }

    if (!editingTask.title.trim()) {
      alert("Task title cannot be empty");
      return;
    }

    try {
      const response = await fetch(
        `${API_URL}/tasks/${editingTask.id}`,
        {
          method: "PUT",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            title: editingTask.title.trim(),
            priority: editingTask.priority,
            due_date:
              editingTask.due_date.trim() || null,
            completed: editingTask.completed,
          }),
        }
      );

      const data = await response.json();

      if (!response.ok) {
        alert(
          data.detail || "Failed to update task"
        );
        return;
      }

      setEditingTask(null);

      await loadTasks(project.id);

      alert("Task updated successfully!");
    } catch (error) {
      console.error("Error updating task:", error);
      alert("Failed to update task");
    }
  };

  // --------------------------------------------------
  // Logout
  // --------------------------------------------------

  const handleLogout = () => {
    localStorage.removeItem("taskflow_user");

    setUser(null);
    setProject(null);
    setTasks([]);

    navigate("/login");
  };

  // --------------------------------------------------
  // Search + Filter + Sort
  // --------------------------------------------------

  const filteredTasks = [...tasks]
    .filter((item) =>
      item.title
        .toLowerCase()
        .includes(search.toLowerCase())
    )
    .filter((item) =>
      priorityFilter === "all"
        ? true
        : item.priority === priorityFilter
    )
    .sort((a, b) => {
      if (sortBy === "title") {
        return a.title.localeCompare(b.title);
      }

      if (sortBy === "priority") {
        const order = {
          high: 1,
          medium: 2,
          low: 3,
        };

        return (
          (order[a.priority] || 99) -
          (order[b.priority] || 99)
        );
      }

      return 0;
    });

  // --------------------------------------------------
  // Statistics
  // --------------------------------------------------

  const totalTasks = tasks.length;

  const completedTasks = tasks.filter(
    (item) => item.completed
  ).length;

  const pendingTasks =
    totalTasks - completedTasks;

  const progressPercentage =
    totalTasks === 0
      ? 0
      : Math.round(
          (completedTasks / totalTasks) * 100
        );

  // --------------------------------------------------
  // Loading
  // --------------------------------------------------

  if (loading) {
    return (
      <div className="taskflow">
        <div
          style={{
            minHeight: "100vh",
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
            fontSize: "20px",
            fontWeight: "600",
          }}
        >
          Loading TaskFlow...
        </div>
      </div>
    );
  }

  // --------------------------------------------------
  // Dashboard
  // --------------------------------------------------

  return (
    <div className="taskflow">

      {/* Navbar */}

      <nav className="navbar">

        <div className="logo">
          TaskFlow
        </div>

        <div className="nav-right">

          {user && (
            <div className="nav-text">
              Welcome,{" "}
              <strong>
                {user.name}
              </strong>
            </div>
          )}

          <button
            className="logout-btn"
            onClick={handleLogout}
          >
            Logout
          </button>

        </div>

      </nav>

      {/* Dashboard */}

      <main className="dashboard">

        <h1 className="dashboard-title">
          TaskFlow Dashboard
        </h1>

        <p className="subtitle">
          Manage your tasks efficiently and stay productive.
        </p>

        {/* Project */}

        {project && (
          <div
            style={{
              marginBottom: "20px",
              fontWeight: "600",
            }}
          >
            Project: {project.name}
          </div>
        )}

        {/* Progress */}

        <div className="progress-card">

          <div className="progress-header">

            <span>
              Task Progress
            </span>

            <strong>
              {progressPercentage}%
            </strong>

          </div>

          <div className="progress-bar">

            <div
              className="progress-fill"
              style={{
                width: `${progressPercentage}%`,
              }}
            />

          </div>

        </div>

        {/* Statistics */}

        <div className="stats">

          <div className="stat-card">

            <h2>
              {totalTasks}
            </h2>

            <p>
              Total Tasks
            </p>

          </div>

          <div className="stat-card">

            <h2>
              {completedTasks}
            </h2>

            <p>
              Completed
            </p>

          </div>

          <div className="stat-card">

            <h2>
              {pendingTasks}
            </h2>

            <p>
              Pending
            </p>

          </div>

        </div>

        {/* Tasks Header */}

        <div className="tasks-header">

          <h2>
            My Tasks
          </h2>

          <button
            className="add-btn"
            onClick={() =>
              setShowForm(true)
            }
          >
            + Add Task
          </button>

        </div>

        {/* Search / Filter / Sort */}

        <div className="filters">

          <input
            type="text"
            placeholder="Search tasks..."
            value={search}
            onChange={(e) =>
              setSearch(e.target.value)
            }
          />

          <select
            value={priorityFilter}
            onChange={(e) =>
              setPriorityFilter(e.target.value)
            }
          >

            <option value="all">
              All Priorities
            </option>

            <option value="high">
              High
            </option>

            <option value="medium">
              Medium
            </option>

            <option value="low">
              Low
            </option>

          </select>

          <select
            value={sortBy}
            onChange={(e) =>
              setSortBy(e.target.value)
            }
          >

            <option value="none">
              Sort By
            </option>

            <option value="title">
              Title
            </option>

            <option value="priority">
              Priority
            </option>

          </select>

        </div>

        {/* Add Task Form */}

        {showForm && (

          <div className="task-form">

            <input
              type="text"
              placeholder="Enter your task"
              value={task}
              onChange={(e) =>
                setTask(e.target.value)
              }
              onKeyDown={(e) => {
                if (e.key === "Enter") {
                  addTask();
                }
              }}
            />

            <button
              className="save-btn"
              onClick={addTask}
            >
              Save Task
            </button>

            <button
              className="cancel-btn"
              onClick={() => {
                setShowForm(false);
                setTask("");
              }}
            >
              Cancel
            </button>

          </div>

        )}

        {/* Edit Form */}

        {editingTask && (

          <div className="edit-form">

            <h3>
              Edit Task
            </h3>

            <input
              type="text"
              value={editingTask.title}
              onChange={(e) =>
                setEditingTask({
                  ...editingTask,
                  title: e.target.value,
                })
              }
            />

            <select
              value={editingTask.priority}
              onChange={(e) =>
                setEditingTask({
                  ...editingTask,
                  priority: e.target.value,
                })
              }
            >

              <option value="low">
                Low
              </option>

              <option value="medium">
                Medium
              </option>

              <option value="high">
                High
              </option>

            </select>

            <input
              type="text"
              placeholder="Due date"
              value={editingTask.due_date}
              onChange={(e) =>
                setEditingTask({
                  ...editingTask,
                  due_date: e.target.value,
                })
              }
            />

            <button
              className="save-btn"
              onClick={saveEdit}
            >
              Save Changes
            </button>

            <button
              className="cancel-btn"
              onClick={() =>
                setEditingTask(null)
              }
            >
              Cancel
            </button>

          </div>

        )}

        {/* Task List */}

        <div>

          {filteredTasks.length === 0 ? (

            <p>
              No tasks found.
            </p>

          ) : (

            filteredTasks.map((item) => (

              <div
                key={item.id}
                className={`task-card ${
                  item.completed
                    ? "completed"
                    : ""
                }`}
              >

                <h3
                  className={`task-title ${
                    item.completed
                      ? "completed"
                      : ""
                  }`}
                >
                  {item.title}
                </h3>

                {/* Priority */}

                <p className="task-info">

                  <strong>
                    Priority:
                  </strong>{" "}

                  <span
                    className={`priority-badge ${item.priority}`}
                  >
                    {item.priority.toUpperCase()}
                  </span>

                </p>

                {/* Details */}

                <div className="task-details">

                  <span className="detail-label">
                    Due:
                  </span>

                  <span className="due-date">
                    {item.due_date || "Not set"}
                  </span>

                  <span className="detail-label">
                    Status:
                  </span>

                  <span
                    className={`status-badge ${
                      item.completed
                        ? "completed"
                        : "pending"
                    }`}
                  >
                    {item.completed
                      ? "COMPLETED"
                      : "PENDING"}
                  </span>

                </div>

                {/* Actions */}

                <div className="task-actions">

                  <button
                    className="complete-btn"
                    onClick={() =>
                      toggleComplete(item)
                    }
                  >
                    {item.completed
                      ? "Mark Pending"
                      : "Complete Task"}
                  </button>

                  <button
                    className="edit-btn"
                    onClick={() =>
                      startEdit(item)
                    }
                  >
                    Edit
                  </button>

                  <button
                    className="delete-btn"
                    onClick={() =>
                      deleteTask(item.id)
                    }
                  >
                    Delete
                  </button>

                </div>

              </div>

            ))

          )}

        </div>

      </main>

    </div>
  );
}

export default App;