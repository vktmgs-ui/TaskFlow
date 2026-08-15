import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import {
  BrowserRouter,
  Routes,
  Route,
  Navigate,
} from "react-router-dom";

import "./index.css";

import App from "./App.jsx";
import Login from "./Login.jsx";
import Signup from "./Signup.jsx";

function ProtectedRoute({ children }) {
  const user = localStorage.getItem("taskflow_user");

  if (!user) {
    return <Navigate to="/login" replace />;
  }

  return children;
}

function MainApp() {
  return (
    <BrowserRouter>
      <Routes>

        {/* Login */}
        <Route
          path="/login"
          element={<Login />}
        />

        {/* Signup */}
        <Route
          path="/signup"
          element={<Signup />}
        />

        {/* Protected Dashboard */}
        <Route
          path="/dashboard"
          element={
            <ProtectedRoute>
              <App />
            </ProtectedRoute>
          }
        />

        {/* Default */}
        <Route
          path="/"
          element={
            <Navigate
              to="/login"
              replace
            />
          }
        />

        {/* Unknown URL */}
        <Route
          path="*"
          element={
            <Navigate
              to="/login"
              replace
            />
          }
        />

      </Routes>
    </BrowserRouter>
  );
}

createRoot(
  document.getElementById("root")
).render(
  <StrictMode>
    <MainApp />
  </StrictMode>
);