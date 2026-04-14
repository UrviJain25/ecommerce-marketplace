import { BrowserRouter, Routes, Route } from "react-router-dom";

import ProtectedRoute from "./ProtectedRoute";

import Login from "../pages/Login";
import Products from "../pages/Products";
import Cart from "../pages/Cart";
import Orders from "../pages/Orders";
import Reviews from "../pages/Review";
import Categories from "../pages/Categories";

export default function AppRoutes() {
  return (
    <BrowserRouter>
      <Routes>

        <Route path="/login" element={<Login />} />

        <Route path="/products" element={
          <ProtectedRoute><Products /></ProtectedRoute>
        } />

        <Route path="/cart" element={
          <ProtectedRoute><Cart /></ProtectedRoute>
        } />

        <Route path="/orders" element={
          <ProtectedRoute><Orders /></ProtectedRoute>
        } />

        <Route path="/reviews" element={
          <ProtectedRoute><Reviews /></ProtectedRoute>
        } />

        <Route path="/categories" element={
          <ProtectedRoute><Categories /></ProtectedRoute>
        } />

      </Routes>
    </BrowserRouter>
  );
}