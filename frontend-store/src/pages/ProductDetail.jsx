import { useEffect, useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { fetchProduct } from '../api';
import { useCart } from '../context/CartContext';

const ProductDetail = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const [product, setProduct] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const { addItem } = useCart();

  useEffect(() => {
    setLoading(true);
    setError(null);
    fetchProduct(id)
      .then(setProduct)
      .catch((err) => setError(err.message || 'Failed to load product')) // Error message is displayed, but must be replaced to avoid exposure of backend bugs
      // .catch((err) => setError('Failed to load product. Please try again later.')) --- IGNORE ---
      .finally(() => setLoading(false));
  }, [id]);

  const handleAddToCart = async () => {
    try {
      await addItem(product.id, 1);
      navigate('/cart');
    } catch (err) {
      alert('Unable to add to cart: ' + err.message); // Error message is displayed, but must be replaced to avoid exposure of backend bugs
      // alert('Unable to add to cart. Please try again later.'); --- IGNORE ---
    }
  };

  if (loading) return <div>Loading product...</div>;
  if (error) return <div className="alert alert-danger">Failed to load product.</div>;
  if (!product) return <div>Product not found.</div>;

  return (
    <div className="row">
      <div className="col-md-6">
        {product.image_url ? (
          <img src={product.image_url} alt={product.name} className="img-fluid rounded" />
        ) : (
          <div className="bg-light border rounded p-5 text-center">No image available</div>
        )}
      </div>
      <div className="col-md-6">
        <h2>{product.name}</h2>
        <p className="text-muted">UGX {product.price.toFixed(2)}</p>
        <p>{product.description || 'No description provided for this product.'}</p>
        <p>
          <strong>Stock:</strong> {product.stock ?? 0}
        </p>
        <button className="btn btn-primary" onClick={handleAddToCart}>
          Add to Cart
        </button>
      </div>
    </div>
  );
};

export default ProductDetail;
