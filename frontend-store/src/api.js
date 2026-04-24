const API_BASE = import.meta.env.VITE_API_URL || 'http://localhost:8000';

async function handleResponse(res) {
  if (!res.ok) {
    let detail;
    try {
      const data = await res.json();
      detail = data.detail || data.message || `${res.status} ${res.statusText}`;
    } catch {
      detail = `${res.status} ${res.statusText}`;
    }
    throw new Error(detail);
  }
  return res.status === 204 ? null : res.json();
}

// ---------- Auth ----------
export const login = () => {
  window.location.href = `${API_BASE}/auth/login`;
};

export const logout = async () => {
  await fetch(`${API_BASE}/auth/logout`, {
    method: 'POST',
    credentials: 'include',
  });
  window.location.href = '/';
};

export const getCurrentUser = async () => {
  const res = await fetch(`${API_BASE}/auth/me`, {
    credentials: 'include',
  });
  if (res.status === 401) return null;
  return handleResponse(res);
};

// ---------- Products ----------
export const fetchProducts = async (skip = 0, limit = 100) => {
  const res = await fetch(`${API_BASE}/products/?skip=${skip}&limit=${limit}`);
  return handleResponse(res);
};

export const fetchProduct = async (id) => {
  const res = await fetch(`${API_BASE}/products/${id}`);
  return handleResponse(res);
};

// ---------- Cart ----------
export const getCart = async () => {
  const res = await fetch(`${API_BASE}/cart/`, {
    credentials: 'include',
  });
  return handleResponse(res);
};

export const addToCart = async (productId, quantity = 1) => {
  const res = await fetch(`${API_BASE}/cart/items`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    credentials: 'include',
    body: JSON.stringify({ product_id: productId, quantity }),
  });
  return handleResponse(res);
};

export const updateCartItem = async (productId, quantity) => {
  const res = await fetch(`${API_BASE}/cart/items/${productId}`, {
    method: 'PUT',
    headers: { 'Content-Type': 'application/json' },
    credentials: 'include',
    body: JSON.stringify({ quantity }),
  });
  return handleResponse(res);
};

export const removeCartItem = async (productId) => {
  const res = await fetch(`${API_BASE}/cart/items/${productId}`, {
    method: 'DELETE',
    credentials: 'include',
  });
  return handleResponse(res);
};

export const clearCart = async () => {
  const res = await fetch(`${API_BASE}/cart/`, {
    method: 'DELETE',
    credentials: 'include',
  });
  return handleResponse(res);
};

// ---------- Orders ----------
export const createOrder = async () => {
  const res = await fetch(`${API_BASE}/orders/`, {
    method: 'POST',
    credentials: 'include',
  });
  return handleResponse(res);
};

export const getOrders = async () => {
  const res = await fetch(`${API_BASE}/orders/`, {
    credentials: 'include',
  });
  return handleResponse(res);
};

export const getOrder = async (orderId) => {
  const res = await fetch(`${API_BASE}/orders/${orderId}`, {
    credentials: 'include',
  });
  return handleResponse(res);
};

export const cancelOrder = async (orderId) => {
  const res = await fetch(`${API_BASE}/orders/${orderId}/cancel`, {
    method: 'POST',
    credentials: 'include',
  });
  return handleResponse(res);
};