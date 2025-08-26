import axios from "axios";

const api = axios.create({
  baseURL: import.meta.env.VITE_API_BASE || "http://localhost:8000",
  timeout: 15000,
});

export async function fetchJobs({ title="", location="", source="", limit=20, offset=0 } = {}) {
  const params = { limit, offset };
  if (title) params.title = title;
  if (location) params.location = location;
  if (source) params.source = source;
  const { data } = await api.get("/jobs", { params });
  return data; // { total, limit, offset, items }
}

export default api;
