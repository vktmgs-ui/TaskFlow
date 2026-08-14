import { useEffect, useState } from "react";
import "./App.css";

const API_URL = "http://127.0.0.1:8000";

function App() {
  const [showForm, setShowForm] = useState(false);
  const [task, setTask] = useState("");
  const [tasks, setTasks] = useState([]);
  const [editingTask, setEditingTask] = useState(null);
  const [search, setSearch] = useState("");
  const [priorityFilter, setPriorityFilter] = useState("all");
  const [sortBy, setSortBy] = useState("none");

  const loadTasks = async () => {
    try {
      const response = await fetch(`${API_URL}/tasks`);

      if (!response.ok) {
        throw new Error("Failed to load tasks");
      }

      const data = await response.json();
      setTasks(data);
    } catch (error) {
      console.error("Error loading tasks:", error);
    }
  };

  useEffect(() => {
    loadTasks();
  }, []);

  const addTask = async () => {
    if (!task.trim()) {
      alert("Please enter a task");
      return;
    }

    try {
      const response = await fetch(`${API_URL}/tasks/quick-add`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          description: task,
          project_id: 1,
        }),
      });

      const data = await response.json();

      if (!response.ok) {
        alert(data.detail || "Failed to add task");
        return;
      }

      alert("Task added successfully!");

      setTask("");
      setShowForm(false);
      loadTasks();
    } catch (error) {
      console.error(error);
      alert("Backend server is not running");
    }
  };

  const toggleComplete = async (item) => {
    try {
      const response = await fetch(`${API_URL}/tasks/${item.id}`, {
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
      });

      if (!response.ok) {
        const data = await response.json();
        alert(data.detail || "Failed to update task");
        return;
      }

      loadTasks();
    } catch (error) {
      console.error(error);
      alert("Failed to update task");
    }
  };

  const deleteTask = async (taskId) => {
    const confirmDelete = window.confirm(
      "Are you sure you want to delete this task?"
    );

    if (!confirmDelete) return;

    try {
      const response = await fetch(`${API_URL}/tasks/${taskId}`, {
        method: "DELETE",
      });

      if (!response.ok) {
        alert("Failed to delete task");
        return;
      }

      loadTasks();
    } catch (error) {
      console.error(error);
      alert("Failed to delete task");
    }
  };

  const startEdit = (item) => {
    setEditingTask({
      id: item.id,
      title: item.title,
      priority: item.priority,
      due_date: item.due_date || "",
      completed: item.completed,
    });
  };

  const saveEdit = async () => {
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
            title: editingTask.title,
            priority: editingTask.priority,
            due_date: editingTask.due_date,
            completed: editingTask.completed,
          }),
        }
      );

      const data = await response.json();

      if (!response.ok) {
        alert(data.detail || "Failed to update task");
        return;
      }

      setEditingTask(null);
      loadTasks();
      alert("Task updated successfully!");
    } catch (error) {
      console.error(error);
      alert("Failed to update task");
    }
  };

  const filteredTasks = tasks
  .filter((item) =>
    item.title.toLowerCase().includes(search.toLowerCase())
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

const totalTasks = tasks.length;

const completedTasks = tasks.filter(
  (item) => item.completed
).length;

const pendingTasks = totalTasks - completedTasks;
  return (
    <div className="taskflow">

      <nav className="navbar">
        <div className="logo">TaskFlow</div>
        <div className="nav-text">Task Management Dashboard</div>
      </nav>

      <main className="dashboard">

        <h1 className="dashboard-title">
          TaskFlow Dashboard
        </h1>

        <p className="subtitle">
          Manage your tasks efficiently and stay productive.
        </p>

        <div className="stats">

          <div className="stat-card">
            <h2>{totalTasks}</h2>
            <p>Total Tasks</p>
          </div>

          <div className="stat-card">
            <h2>{completedTasks}</h2>
            <p>Completed</p>
          </div>

          <div className="stat-card">
            <h2>{pendingTasks}</h2>
            <p>Pending</p>
          </div>

        </div>

        <div className="tasks-header">
          <h2>My Tasks</h2>

          <button
            className="add-btn"
            onClick={() => setShowForm(true)}
          >
            + Add Task
          </button>
         <div className="filters">
  <input
    type="text"
    placeholder="Search tasks..."
    value={search}
    onChange={(e) => setSearch(e.target.value)}
    <input
  type="text"
  placeholder="Search tasks..."
  value={search}
  onChange={(e) => setSearch(e.target.value)}
/>

  <select
    value={priorityFilter}
    onChange={(e) => setPriorityFilter(e.target.value)}
    
  >
    <option value="all">All Priorities</option>
    <option value="high">High</option>
    <option value="medium">Medium</option>
    <option value="low">Low</option>
  </select>

  <select
    value={sortBy}
    onChange={(e) => setSortBy(e.target.value)}
    
  >
    <option value="none">Sort By</option>
    <option value="title">Title</option>
    <option value="priority">Priority</option>
  </select>
</div>
        </div>

        {showForm && (
          <div className="task-form">

            <input
              type="text"
              placeholder="Enter your task"
              value={task}
              onChange={(e) => setTask(e.target.value)}
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

        {editingTask && (
          <div className="edit-form">

            <h3>Edit Task</h3>

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
              <option value="low">Low</option>
              <option value="medium">Medium</option>
              <option value="high">High</option>
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
              onClick={() => setEditingTask(null)}
            >
              Cancel
            </button>

          </div>
        )}

        <div>

          {tasks.length === 0 ? (
            <p>No tasks found.</p>
          ) : (
           filteredTasks.map((item) => (

              <div
                key={item.id}
                className={`task-card ${
                  item.completed ? "completed" : ""
                }`}
              >

                <h3
                  className={`task-title ${
                    item.completed ? "completed" : ""
                  }`}
                >
                  {item.title}
                </h3>

                <p className="task-info">
                  <strong>Priority:</strong>{" "}
                  {item.priority}
                </p>

                <p className="task-info">
                  <strong>Due:</strong>{" "}
                  {item.due_date || "Not set"}
                </p>

                <p className="task-info">
                  <strong>Status:</strong>{" "}
                  {item.completed
                    ? "Completed"
                    : "Pending"}
                </p>

                <button
                  className="complete-btn"
                  onClick={() => toggleComplete(item)}
                >
                  {item.completed
                    ? "Mark Pending"
                    : "Complete Task"}
                </button>

                <button
                  className="edit-btn"
                  onClick={() => startEdit(item)}
                >
                  Edit
                </button>

                <button
                  className="delete-btn"
                  onClick={() => deleteTask(item.id)}
                >
                  Delete
                </button>

              </div>

            ))
          )}

        </div>

      </main>
    </div>
  );
}

export default App;