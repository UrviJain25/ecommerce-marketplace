import { useEffect, useState } from "react";
import { getRecommendations } from "../api/recommendations";
import { handleApiError } from "../api/axios";

export default function Recommendations() {
  const [results, setResults] = useState<any[]>([]);
  const [message, setMessage] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(true);

  const fetchRecommendations = async () => {
    try {
      const data = await getRecommendations();

      setResults(data?.data || []);
      setMessage(data?.message || "");
      setError("");
    } catch (err: any) {
      setError(handleApiError(err));
    } finally {
      setLoading(false);
    }
  };

  // AUTO LOAD on page open
  useEffect(() => {
    fetchRecommendations();
  }, []);

  return (
    <div className="p-10">

      <h1 className="text-3xl font-bold mb-6">
        Recommendations
      </h1>

      {/* LOADING */}
      {loading && (
        <p className="text-gray-500">Loading recommendations...</p>
      )}

      {/* ERROR */}
      {error && (
        <p className="text-red-500 mb-4">
          {error}
        </p>
      )}

      {/* MESSAGE */}
      {message && (
        <p className="text-green-600 mb-4">
          {message}
        </p>
      )}

      {/* RESULTS */}
      {!loading && results.length === 0 && (
        <p className="text-gray-500">
          No recommendations yet
        </p>
      )}

      <div className="grid grid-cols-3 gap-6">

        {results.map((item) => (
          <div key={item.id} className="border p-4 rounded shadow">

            <h2 className="font-bold text-lg mb-2">
              {item.name}
            </h2>

            <p className="text-gray-700 mb-1">
              ${item.price}
            </p>

            <p className="text-sm text-gray-500">
              Stock: {item.stock_qty}
            </p>

          </div>
        ))}

      </div>

    </div>
  );
}