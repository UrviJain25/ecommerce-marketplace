import { useState } from "react";
import { getProducts } from "../api/products";
import { handleApiError } from "../api/axios";
import { addToCart } from "../api/cart";
import { useNavigate } from "react-router-dom";

export default function Products() {
  const navigate = useNavigate();

  const [search, setSearch] = useState("");
  const [minPrice, setMinPrice] = useState<number | undefined>();
  const [maxPrice, setMaxPrice] = useState<number | undefined>();
  const [categoryId, setCategoryId] = useState<number | undefined>();

  const [products, setProducts] = useState<any[]>([]);
  const [error, setError] = useState("");

  const handleAddToCart = async (productId: number) => {
    try {
      await addToCart(productId, 1);
      alert("✅ Added to cart");
    } catch (err: any) {
      alert(handleApiError(err));
    }
  };

  const handleFetch = async () => {
  try {
    // frontend validation
    if (
      minPrice !== undefined &&
      maxPrice !== undefined &&
      minPrice > maxPrice
    ) {
      setError("Min price cannot be greater than max price");
      return;
    }

    if (search && search.length < 2) {
      setError("Search must be at least 2 characters");
      return;
    }

    const data = await getProducts({
      search,
      min_price: minPrice,
      max_price: maxPrice,
      category_id: categoryId,
    });
    if(data.length==0) setError("No search results")
    else setError(""); // clear error on success
    setProducts(data);
    
  } catch (err: any) {
  console.log("SEARCH ERROR:", err.response?.data);

  const data = err.response?.data;

  const backendMsg =
    typeof data?.detail === "string"
      ? data.detail
      : data?.detail?.[0]?.msg ||
        data?.message ||
        err.message ||
        "Something went wrong";

  setError(backendMsg);
}
};

  return (
    <div className="p-10">

      <h1 className="text-3xl font-bold mb-6">
        Products
      </h1>

      {error && <p className="text-red-500 mb-4">{error}</p>}

      {/* Filters */}
      <div className="grid grid-cols-4 gap-4 mb-6">

        <input
          placeholder="Search"
          className="border p-2"
          onChange={(e) => setSearch(e.target.value)}
        />

        <input
          type="number"
          placeholder="Min Price"
          className="border p-2"
          onChange={(e) => setMinPrice(Number(e.target.value))}
        />

        <input
          type="number"
          placeholder="Max Price"
          className="border p-2"
          onChange={(e) => setMaxPrice(Number(e.target.value))}
        />

        <input
          type="number"
          placeholder="Category ID"
          className="border p-2"
          onChange={(e) => setCategoryId(Number(e.target.value))}
        />

      </div>

      <button
        onClick={handleFetch}
        className="bg-blue-500 text-white px-6 py-2 mb-6"
      >
        Load Products
      </button>

      {/* Products */}
      <div className="grid grid-cols-3 gap-6">

        {products.map((p) => (
          <div key={p.id} className="border p-4">

            <h2 className="font-bold">{p.name}</h2>
            <p>Price: ${p.price}</p>
            <p>Stock: {p.stock_qty}</p>

            {/* ACTION BUTTONS */}
            <div className="flex gap-2 mt-2 flex-wrap">

              <button
                onClick={() => handleAddToCart(p.id)}
                className="bg-green-500 text-white px-3 py-1"
              >
                Add to Cart
              </button>

              <button
                onClick={() => navigate(`/products/${p.id}/reviews`)}
                className="bg-blue-500 text-white px-3 py-1"
              >
                Reviews
              </button>

              <button
                onClick={() => navigate(`/review/${p.id}`)}
                className="bg-purple-500 text-white px-3 py-1"
              >
                Add Review
              </button>

            </div>

          </div>
        ))}

      </div>

    </div>
  );
}