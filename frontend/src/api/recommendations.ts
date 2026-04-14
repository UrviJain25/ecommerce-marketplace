import API from "./axios";

export const getRecommendations = async () => {
  const res = await API.get("/recommendations");
  return res.data;
};