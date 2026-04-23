// src/components/NavigationBar.jsx
import { useEffect, useState } from 'react';
import { getCurrentUser, logout, login } from '../api';
import { useCart } from '../context/CartContext';

const NavigationBar = () => {
  const [user, setUser] = useState(null);
  const { cartCount } = useCart();

  useEffect(() => {
    getCurrentUser().then(setUser);
  }, []);

  const handleLogout = async () => {
    await logout();
    setUser(null);
  };

  return (
    <nav className="navbar navbar-expand-lg navbar-light bg-light">
      <div className="container">
        <a className="navbar-brand" href="/">Limelight Store</a>
        <button className="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav">
          <span className="navbar-toggler-icon"></span>
        </button>
        <div className="collapse navbar-collapse" id="navbarNav">
          <ul className="navbar-nav ms-auto">
            <li className="nav-item"><a className="nav-link" href="/shop">Shop</a></li>
            <li className="nav-item"><a className="nav-link" href="/cart">Cart ({cartCount})</a></li>
            {user ? (
              <>
                <li className="nav-item"><span className="nav-link">Hello, {user.name}</span></li>
                <li className="nav-item"><button className="btn btn-outline-danger btn-sm" onClick={handleLogout}>Logout</button></li>
              </>
            ) : (
              <li className="nav-item"><button className="btn btn-primary btn-sm" onClick={login}>Login</button></li>
            )}
          </ul>
        </div>
      </div>
    </nav>
  );
};

export default NavigationBar;