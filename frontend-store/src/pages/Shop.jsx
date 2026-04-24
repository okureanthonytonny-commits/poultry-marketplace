import { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { fetchProducts } from '../api';
import { useCart } from '../context/CartContext';

const Shop = () => {
  const [products, setProducts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const { addItem } = useCart();

  useEffect(() => {
    fetchProducts()
      .then(setProducts)
      .catch((err) => setError(err.message || 'Failed to load products')) // Error message is displayed, but must be replaced to avoid exposure of backend bugs
      .finally(() => setLoading(false));
  }, []);

  if (loading) return <div>Loading products...</div>;
  if (error) return <div className="alert alert-danger">Failed to load products.</div>;

  return (
    <div>
      <h2>Products</h2>
      <div className="row">
        {products.map(product => (
          <div key={product.id} className="col-md-4 mb-3">
            <div className="card h-100">
              {product.image_url && (
                <img src={product.image_url} className="card-img-top" alt={product.name} />
              )}
              <div className="card-body d-flex flex-column">
                <h5 className="card-title">{product.name}</h5>
                <p className="card-text text-truncate">{product.description || 'No description available.'}</p>
                <p className="fw-bold">UGX {product.price.toFixed(2)}</p>
                <div className="mt-auto d-flex justify-content-between align-items-center">
                  <button
                    className="btn btn-primary"
                    onClick={() => addItem(product.id, 1)}
                  >
                    Add to Cart
                  </button>
                  <Link className="btn btn-link" to={`/product/${product.id}`}>
                    View
                  </Link>
                </div>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default Shop;