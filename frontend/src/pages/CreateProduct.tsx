import { useState, useEffect } from "react";
import { createProduct } from "../api/products";
import { useNavigate } from "react-router-dom";
import { getMe } from "../api/auth";

export default function CreateProduct() {
  const [form, setForm] = useState({
    name: "",
    description: "",
    price: "",
    stock_qty: "",
    category_id: "",
  });

  const [userId, setUserId] = useState<number | null>(null);
  const [error, setError] = useState("");

  const navigate = useNavigate();

  // Fetch logged-in user
  useEffect(() => {
    const fetchUser = async () => {
      try {
        const user = await getMe();
        setUserId(user.id);
      } catch (err) {
        console.log("Failed to fetch user");
        setError("User not authenticated");
      }
    };

    fetchUser();
  }, []);

  const handleSubmit = async () => {
    try {
      // validation
      if (!form.name || !form.price) {
        setError("Name and price are required");
        return;
      }

      if (!userId) {
        setError("User not loaded yet");
        return;
      }

      const payload = {
        name: form.name,
        description: form.description,
        price: parseFloat(form.price),
        stock_qty: form.stock_qty ? parseInt(form.stock_qty) : 0,
        seller_id: userId,

        category_id: form.category_id
          ? parseInt(form.category_id)
          : null,
      };

      console.log("SENDING:", payload);

      await createProduct(payload);

      navigate("/my-products");
    } catch (err: any) {
      console.log("FULL ERROR:", err.response?.data);

      const detail = err.response?.data?.detail?.[0];

      const msg =
        detail?.msg ||
        err.response?.data?.detail ||
        err.message ||
        "Something went wrong";

      setError(typeof msg === "string" ? msg : JSON.stringify(msg));
    }
  };

  return (
    <div className="p-10">
      <h1 className="text-xl font-bold mb-4">Create Product</h1>

      {error && <p className="text-red-500 mb-4">{error}</p>}

      <input
        value={form.name}
        placeholder="Name"
        className="border p-2 block mb-2"
        onChange={(e) =>
          setForm({ ...form, name: e.target.value })
        }
      />

      <input
        value={form.description}
        placeholder="Description"
        className="border p-2 block mb-2"
        onChange={(e) =>
          setForm({ ...form, description: e.target.value })
        }
      />

      <input
        value={form.price}
        placeholder="Price"
        type="number"
        className="border p-2 block mb-2"
        onChange={(e) =>
          setForm({ ...form, price: e.target.value })
        }
      />

      <input
        value={form.stock_qty}
        placeholder="Stock Quantity"
        type="number"
        className="border p-2 block mb-2"
        onChange={(e) =>
          setForm({ ...form, stock_qty: e.target.value })
        }
      />

      <input
        value={form.category_id}
        placeholder="Category ID (optional)"
        type="number"
        className="border p-2 block mb-4"
        onChange={(e) =>
          setForm({ ...form, category_id: e.target.value })
        }
      />

      <button
        onClick={handleSubmit}
        className="bg-blue-500 text-white px-4 py-2"
      >
        Create
      </button>
    </div>
  );
}