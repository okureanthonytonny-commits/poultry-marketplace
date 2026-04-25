import { useCart } from '../context/CartContext';
import { createOrder } from '../api';
import { useNavigate } from 'react-router-dom';

const Cart = () => {
  const { cart, updateItem, removeItem, clear } = useCart();
  const navigate = useNavigate();

  const handlePlaceOrder = async () => {
    try {
      await createOrder();
      alert('Order placed!');
      navigate('/orders');
    } catch (err) {
      alert('Failed to place order: ' + err.message); // Error message is displayed, but must be replaced to avoid exposure of backend bugs
      // alert('Failed to place order. Please try again later.'); --- IGNORE ---
    }
  };

  if (cart.length === 0) return <div>Your cart is empty.</div>;

  return (
    <div>
      <h2>Shopping Cart</h2>
      <table className="table">
        <thead>
          <tr>
            <th>Product</th>
            <th>Price</th>
            <th>Quantity</th>
            <th>Total</th>
            <th></th>
          </tr>
        </thead>
        <tbody>
          {cart.map(item => (
            <tr key={item.product_id}>
              <td>{item.product_name}</td>
              <td>{item.product_price}</td>
              <td>
                <input
                  type="number"
                  value={item.quantity}
                  onChange={e => updateItem(item.product_id, parseInt(e.target.value) || 1)}
                  className="form-control"
                  style={{ width: '80px' }}
                />
              </td>
              <td>{(item.product_price * item.quantity).toFixed(2)}</td>
              <td>
                <button className="btn btn-danger btn-sm" onClick={() => removeItem(item.product_id)}>Remove</button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
      <button className="btn btn-secondary" onClick={clear}>Clear Cart</button>
      <button className="btn btn-primary ms-2" onClick={handlePlaceOrder}>Place Order</button>
    </div>
  );
};

export default Cart;