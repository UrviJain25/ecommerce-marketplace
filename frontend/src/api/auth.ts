import api from "./axios";

export const registerUser = async (data: any) => {
  const res = await api.post("/auth/auth/register", data);
  return res.data;
};

export const loginUser = async (data: any) => {
  const res = await api.post("/auth/auth/login", data);
  return res.data;
};

export const getMe = async () => {
  const res = await api.get("/auth/auth/me");
  return res.data;
};

export const getUserRole = () => {
  const user = localStorage.getItem("user");
  if (!user) return null;

  try {
    return JSON.parse(user).role;
  } catch {
    return null;
  }
};