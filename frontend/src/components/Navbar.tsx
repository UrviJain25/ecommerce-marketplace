import { Link, useNavigate } from "react-router-dom";
import { useEffect, useState } from "react";
import { getMe } from "../api/auth";

export default function Navbar() {
  const navigate = useNavigate();

  const [role, setRole] = useState<string | null>(null);

  // Fetch role
  useEffect(() => {
    const fetchUser = async () => {
      try {
        const user = await getMe();
        setRole(user.role);
      } catch {
        setRole(null);
      }
    };

    fetchUser();
  }, []);

  const logout = () => {
    localStorage.removeItem("token");
    localStorage.removeItem("user");
    window.location.href = "/login";
  };

  return (
    <nav className="bg-gray-900 text-white px-6 py-4 flex gap-4 items-center">

      {/* LEFT */}
      <Link to="/" className="font-bold text-lg">
        🛒 E-Commerce Store
      </Link>

      <Link to="/products">Products</Link>
      <Link to="/cart">Cart</Link>
      <Link to="/orders">Orders</Link>
      <Link to="/profile">Profile</Link>

      {/* SELLER + ADMIN */}
      {(role === "seller" || role === "admin") && (
        <Link to="/my-products">My Products</Link>
      )}

      {/* ADMIN ONLY */}
      {role === "admin" && (
        <>
          <Link to="/categories">Categories</Link>
          <Link to="/reports">Reports</Link>
        </>
      )}

      {/* RIGHT */}
      <div className="ml-auto flex gap-3">

          <button
            onClick={() => navigate("/recommendations")}
            className="bg-purple-500 px-3 py-1 rounded hover:bg-purple-600"
          >
            AI Recs
          </button>

        <button
          onClick={logout}
          className="bg-red-500 px-3 py-1 rounded hover:bg-red-600"
        >
          Logout
        </button>

      </div>
    </nav>
  );
}