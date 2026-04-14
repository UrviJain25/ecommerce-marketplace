import { Routes, Route, Navigate } from "react-router-dom";

// Pages
import Login from "./pages/Login";
import Register from "./pages/Register";
import Products from "./pages/Products";
import Search from "./pages/Search";
import Profile from "./pages/Profile";
import CreateProduct from "./pages/CreateProduct";
import MyProducts from "./pages/MyProducts";
import EditProduct from "./pages/EditProduct";
import ProductReviews from "./pages/ProductReviews";
import Review from "./pages/Review";
import Recommendations from "./pages/Recommendations";
import Reports from "./pages/Reports";
import Cart from "./pages/Cart";
import Orders from "./pages/Orders";
import Categories from "./pages/Categories";

// Components
import ProtectedRoute from "./routes/ProtectedRoute";
import Navbar from "./components/Navbar";

export default function App() {
  const isLoggedIn = !!localStorage.getItem("token");

  return (
    <>
      {/* ✅ Navbar only when logged in */}
      {isLoggedIn && <Navbar />}

      <Routes>
        {/* DEFAULT */}
        <Route
          path="/"
          element={<Navigate to="/login" replace />}
        />

        {/* PUBLIC */}
        <Route
          path="/login"
          element={!isLoggedIn ? <Login /> : <Navigate to="/products" />}
        />
        <Route
          path="/register"
          element={!isLoggedIn ? <Register /> : <Navigate to="/products" />}
        />

        {/* PROTECTED (ALL USERS) */}
        <Route
          path="/products"
          element={
            <ProtectedRoute>
              <Products />
            </ProtectedRoute>
          }
        />

        <Route
          path="/cart"
          element={
            <ProtectedRoute>
              <Cart />
            </ProtectedRoute>
          }
        />

        <Route
          path="/orders"
          element={
            <ProtectedRoute>
              <Orders />
            </ProtectedRoute>
          }
        />

        <Route
          path="/search"
          element={
            <ProtectedRoute>
              <Search />
            </ProtectedRoute>
          }
        />

        <Route
          path="/profile"
          element={
            <ProtectedRoute>
              <Profile />
            </ProtectedRoute>
          }
        />

        <Route
          path="/recommendations"
          element={
            <ProtectedRoute>
              <Recommendations />
            </ProtectedRoute>
          }
        />

        {/* REVIEWS */}
        <Route
          path="/products/:id/reviews"
          element={
            <ProtectedRoute>
              <ProductReviews />
            </ProtectedRoute>
          }
        />

        <Route
          path="/review/:id"
          element={
            <ProtectedRoute>
              <Review />
            </ProtectedRoute>
          }
        />
        
        {/* SELLER + ADMIN */}
        <Route
          path="/my-products"
          element={
            <ProtectedRoute allowedRoles={["seller", "admin"]}>
              <MyProducts />
            </ProtectedRoute>
          }
        />

        <Route
          path="/create-product"
          element={
            <ProtectedRoute allowedRoles={["seller", "admin"]}>
              <CreateProduct />
            </ProtectedRoute>
          }
        />

        <Route
          path="/edit/:id"
          element={
            <ProtectedRoute allowedRoles={["seller", "admin"]}>
              <EditProduct />
            </ProtectedRoute>
          }
        />

        {/*ADMIN ONLY */}
        <Route
          path="/categories"
          element={
            <ProtectedRoute allowedRoles={["admin"]}>
              <Categories />
            </ProtectedRoute>
          }
        />

        <Route
          path="/reports"
          element={
            <ProtectedRoute allowedRoles={["admin"]}>
              <Reports />
            </ProtectedRoute>
          }
        />

        {/* 404 */}
        <Route
          path="*"
          element={
            <div className="p-10 text-center text-xl font-bold">
              404 - Page Not Found
            </div>
          }
        />
      </Routes>
    </>
  );
}