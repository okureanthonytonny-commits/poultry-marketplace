import { useEffect, useState } from 'react';
import { useParams, Link } from 'react-router-dom';
import { getOrder } from '../api';

const OrderDetail = () => {
  const { id } = useParams();
  const [order, setOrder] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    getOrder(id)
      .then(setOrder)
      .catch((err) => setError(err.message || 'Failed to load order')) // Error message is displayed, but must be replaced to avoid exposure of backend bugs
      // .catch((err) => setError('Failed to load order. Please try again later.')) --- IGNORE ---
      .finally(() => setLoading(false));
  }, [id]);

  if (loading) return <div>Loading order...</div>;
  if (error) return <div className="alert alert-danger">Failed to load order.</div>;
  if (!order) return <div>Order not found.</div>;

  const total = order.items.reduce((sum, item) => sum + item.price_snapshot * item.quantity, 0);

  return (
    <div>
      <div className="d-flex justify-content-between align-items-center mb-4">
        <div>
          <h2>Order #{order.id}</h2>
          <p className="mb-1">Status: {order.status}</p>
          <p className="text-muted">Placed on {new Date(order.created_at).toLocaleString()}</p>
        </div>
        <Link className="btn btn-outline-secondary" to="/orders">Back to orders</Link>
      </div>

      <div className="table-responsive">
        <table className="table">
          <thead>
            <tr>
              <th>Product</th>
              <th>Price</th>
              <th>Quantity</th>
              <th>Total</th>
            </tr>
          </thead>
          <tbody>
            {order.items.map(item => (
              <tr key={item.id}>
                <td>{item.product_name}</td>
                <td>UGX {item.price_snapshot.toFixed(2)}</td>
                <td>{item.quantity}</td>
                <td>UGX {(item.price_snapshot * item.quantity).toFixed(2)}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      <div className="mt-4">
        <strong>Total:</strong> UGX {total.toFixed(2)}
      </div>
    </div>
  );
};

export default OrderDetail;
