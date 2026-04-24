import { Link } from 'react-router-dom';

const Home = () => (
  <div className="text-center py-5">
    <h1>Welcome to Limelight Store</h1>
    <p className="lead">
      Shop fresh products, manage your cart, and review your orders.
    </p>
    <div className="d-flex justify-content-center gap-2">
      <Link className="btn btn-primary btn-lg" to="/shop">
        Start Shopping
      </Link>
      <Link className="btn btn-outline-secondary btn-lg" to="/orders">
        View Orders
      </Link>
    </div>
  </div>
);

export default Home;
