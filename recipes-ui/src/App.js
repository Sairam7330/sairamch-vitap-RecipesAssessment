import axios from "axios";
import { useEffect, useState } from "react";

function App() {
  const [recipes, setRecipes] = useState([]);
  const [page, setPage] = useState(1);
  const [limit] = useState(10);
  const [total, setTotal] = useState(0);
  const [search, setSearch] = useState("");
  const [cuisine, setCuisine] = useState("");
  const [minRating, setMinRating] = useState("");

  useEffect(() => {
    fetchRecipes();
  }, [page]);

  const fetchRecipes = async () => {
    try {
      const res = await axios.get(
        `http://127.0.0.1:5000/api/recipes?page=${page}&limit=${limit}`
      );
      setRecipes(res.data.data);
      setTotal(res.data.total);
    } catch (err) {
      console.error("Error fetching recipes:", err);
    }
  };

  const searchRecipes = async () => {
    try {
      const res = await axios.get("http://127.0.0.1:5000/api/recipes/search", {
        params: { title: search, cuisine, rating: minRating },
      });
      setRecipes(res.data.data);
      setTotal(res.data.data.length);
      setPage(1);
    } catch (err) {
      console.error("Error searching recipes:", err);
    }
  };

  return (
    <div style={{ padding: "20px" }}>
      <h1>🍲 Recipe Explorer</h1>

      {/* Search Filters */}
      <div style={{ marginBottom: "20px" }}>
        <input
          type="text"
          placeholder="Search title..."
          value={search}
          onChange={(e) => setSearch(e.target.value)}
        />
        <input
          type="text"
          placeholder="Cuisine..."
          value={cuisine}
          onChange={(e) => setCuisine(e.target.value)}
        />
        <input
          type="number"
          placeholder="Min Rating"
          value={minRating}
          onChange={(e) => setMinRating(e.target.value)}
        />
        <button onClick={searchRecipes}>🔍 Search</button>
        <button onClick={fetchRecipes}>🔄 Reset</button>
      </div>

      {/* Recipes Table */}
      <table border="1" cellPadding="10" style={{ width: "100%" }}>
        <thead>
          <tr>
            <th>Title</th>
            <th>Cuisine</th>
            <th>Rating</th>
            <th>Total Time</th>
            <th>Serves</th>
          </tr>
        </thead>
        <tbody>
          {recipes.map((r) => (
            <tr key={r.id}>
              <td>{r.title}</td>
              <td>{r.cuisine}</td>
              <td>{r.rating}</td>
              <td>{r.total_time}</td>
              <td>{r.serves}</td>
            </tr>
          ))}
        </tbody>
      </table>

      {/* Pagination */}
      <div style={{ marginTop: "20px" }}>
        <button onClick={() => setPage((p) => Math.max(p - 1, 1))} disabled={page === 1}>
          ◀ Prev
        </button>
        <span style={{ margin: "0 10px" }}>
          Page {page} of {Math.ceil(total / limit)}
        </span>
        <button
          onClick={() => setPage((p) => p + 1)}
          disabled={page * limit >= total}
        >
          Next ▶
        </button>
      </div>
    </div>
  );
}

export default App;
