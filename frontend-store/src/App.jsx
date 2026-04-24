import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import NavigationBar from './components/NavigationBar';
import { UserProvider } from './context/UserContext';
import { CartProvider } from './context/CartContext';

// Temporary placeholder pages (we will replace these later)
const Home = () => <h2 className='text-center mt-1'>Home page</h2>;
const Shop = () => <h2 className='text-center mt-1'>Shop page</h2>;
const ProductDetail = () => <h2 className='text-center mt-1'>Product Detail page</h2>;
const Cart = () => <h2 className='text-center mt-1'>Cart page</h2>;
const Orders = () => <h2 className='text-center mt-1'>Orders page</h2>;
const OrderDetail = () => <h2 className='text-center mt-1'>Order Detail page</h2>;

function App() {
  return (
    <UserProvider>
      <CartProvider>
        <Router>
          <NavigationBar />
          <main className="container mt-4">
            <Routes>
              <Route path="/" element={<Home />} />
              <Route path="/shop" element={<Shop />} />
              <Route path="/product/:id" element={<ProductDetail />} />
              <Route path="/cart" element={<Cart />} />
              <Route path="/orders" element={<Orders />} />
              <Route path="/orders/:id" element={<OrderDetail />} />
            </Routes>
          </main>
        </Router>
      </CartProvider>
    </UserProvider>
  );
}

export default App;