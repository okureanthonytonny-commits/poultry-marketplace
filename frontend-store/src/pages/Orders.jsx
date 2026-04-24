import { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { getOrders } from '../api';

const Orders = () => {
  const [orders, setOrders] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    getOrders()
      .then(setOrders)
      .catch((err) => setError(err.message || 'Failed to load orders')) // Error message is displayed, but must be replaced to avoid exposure of backend bugs
      // .catch((err) => setError('Failed to load orders. Please try again later.')) --- IGNORE ---
      .finally(() => setLoading(false));
  }, []);

  if (loading) return <div>Loading orders...</div>;
  if (error) return <div className="alert alert-danger">Failed to load orders.</div>;
  if (orders.length === 0) return (
    <div>
      <p>You have no orders yet.</p>
      <Link className="btn btn-primary" to="/shop">Browse products</Link>
    </div>
  );

  return (
    <div>
      <h2>My Orders</h2>
      <div className="table-responsive">
        <table className="table">
          <thead>
            <tr>
              <th>Order</th>
              <th>Status</th>
              <th>Items</th>
              <th>Total</th>
              <th></th>
            </tr>
          </thead>
          <tbody>
            {orders.map(order => {
              const total = order.items.reduce((sum, item) => sum + item.price_snapshot * item.quantity, 0);
              return (
                <tr key={order.id}>
                  <td>#{order.id}</td>
                  <td>{order.status}</td>
                  <td>{order.items.length}</td>
                  <td>UGX {total.toFixed(2)}</td>
                  <td>
                    <Link className="btn btn-link" to={`/orders/${order.id}`}>
                      View
                    </Link>
                  </td>
                </tr>
              );
            })}
          </tbody>
        </table>
      </div>
    </div>
  );
};

export default Orders;
