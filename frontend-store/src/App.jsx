import { useState, useEffect } from 'react';
import { fetchItems, createItem } from './features/auth/api';
import 'bootstrap/dist/css/bootstrap.min.css';

function App() {
  const [items, setItems] = useState([]);
  const [newItem, setNewItem] = useState('');
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    fetchItems().then(setItems).catch(console.error);
  }, []);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!newItem.trim()) return;
    setLoading(true);
    try {
      const created = await createItem(newItem);
      setItems([...items, created]);
      setNewItem('');
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="container mt-4">
      <h1>Test Items</h1>
      <ul className="list-group mb-3">
        {items.map(item => (
          <li key={item.id} className="list-group-item">
            {item.name} <small className="text-muted">({new Date(item.created_at).toLocaleString()})</small>
          </li>
        ))}
      </ul>
      <form onSubmit={handleSubmit}>
        <div className="input-group">
          <input
            type="text"
            className="form-control"
            placeholder="Item name"
            value={newItem}
            onChange={e => setNewItem(e.target.value)}
            disabled={loading}
          />
          <button className="btn btn-primary" type="submit" disabled={loading}>
            Add Item
          </button>
        </div>
      </form>
    </div>
  );
}

export default App;