import { useEffect, useState } from "react";
import axios from "axios";
import { handleApiError } from "../api/axios";

export default function Categories() {
  const [categories, setCategories] = useState<any[]>([]);
  const [name, setName] = useState("");
  const [error, setError] = useState("");

  //attach token manually
  const getHeaders = () => ({
    Authorization: `Bearer ${localStorage.getItem("token")}`,
  });

  const load = async () => {
    try {
      const res = await axios.get(
        "http://localhost:8000/categories/categories/"
      );
      setCategories(res.data);
    } catch (err: any) {
      setError(handleApiError(err));
    }
  };

  const create = async () => {
    try {
      await axios.post(
        "http://localhost:8000/categories/categories/",
        { name },
        { headers: getHeaders() }
      );
      setName("");
      load();
    } catch (err: any) {
      setError(handleApiError(err));
    }
  };

  const remove = async (id: number) => {
    try {
      await axios.delete(
        `http://localhost:8000/categories/categories/${id}`,
        { headers: getHeaders() }
      );
      load();
    } catch (err: any) {
      setError(handleApiError(err));
    }
  };

  useEffect(() => {
    load();
  }, []);

  return (
    <div className="p-10">
      <h1 className="text-xl font-bold mb-4">Categories</h1>

      {error && <p className="text-red-500 mb-3">{error}</p>}

      <div className="mb-4">
        <input
          value={name}
          onChange={(e) => setName(e.target.value)}
          placeholder="New category"
          className="border p-2 mr-2"
        />
        <button
          onClick={create}
          className="bg-blue-500 text-white px-3 py-2"
        >
          Add
        </button>
      </div>

      {categories.map((c) => (
        <div key={c.id} className="flex justify-between mt-3 border p-2">
          <span>{c.name}</span>
          <button
            onClick={() => remove(c.id)}
            className="bg-red-500 text-white px-2"
          >
            Delete
          </button>
        </div>
      ))}
    </div>
  );
}