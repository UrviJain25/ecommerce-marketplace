import { Navigate } from "react-router-dom";
import { getUserRole } from "../api/auth";

export default function ProtectedRoute({ children, allowedRoles }: any) {
  const token = localStorage.getItem("token");
  const role = getUserRole();

  if (!token || token === "undefined" || token === "null") {
    return <Navigate to="/login" replace />;
  }

  if (allowedRoles && !allowedRoles.includes(role)) {
    return <Navigate to="/products" />;
  }

  return children;
}