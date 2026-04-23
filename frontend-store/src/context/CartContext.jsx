// src/context/CartContext.jsx
import { createContext, useState, useContext, useEffect } from 'react';
import { getCart, addToCart, updateCartItem, removeCartItem, clearCart } from '../api';

const CartContext = createContext();

export const CartProvider = ({ children }) => {
  const [cart, setCart] = useState([]);
  const [loading, setLoading] = useState(true);

  const fetchCart = async () => {
    try {
      const data = await getCart();
      setCart(data);
    } catch (err) {
      console.error('Failed to fetch cart', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchCart();
  }, []);

  const addItem = async (productId, quantity) => {
    const newItem = await addToCart(productId, quantity);
    setCart(prev => [...prev, newItem]);
  };

  const updateItem = async (productId, quantity) => {
    const updated = await updateCartItem(productId, quantity);
    setCart(prev => prev.map(item => item.product_id === productId ? updated : item));
  };

  const removeItem = async (productId) => {
    await removeCartItem(productId);
    setCart(prev => prev.filter(item => item.product_id !== productId));
  };

  const clear = async () => {
    await clearCart();
    setCart([]);
  };

  const cartCount = cart.reduce((total, item) => total + item.quantity, 0);

  return (
    <CartContext.Provider value={{ cart, loading, addItem, updateItem, removeItem, clear, cartCount }}>
      {children}
    </CartContext.Provider>
  );
};

export const useCart = () => useContext(CartContext);