import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import NavigationBar from './components/NavigationBar';

// Temporary placeholder pages (we will move these to /src/pages later)
const Checkout = () => <h2 className="text-center mt-5">Checkout Form</h2>;
const Home = () => <h2 className='text-center mt-1'>Home page</h2>;
const Shop = () => <h2 className='text-center mt-1'>Shop page</h2>;
const ProductDetail = () => <h2 className='text-center mt-1'>Product Detail page</h2>;  

function App() {
  return (
    <Router>
      {/* 1. Base Layout: NavBar stays outside Routes so it never unmounts */}
      <NavigationBar />

      {/* 2. Page Content: Only this section changes when clicking links */}
      <main className="container mt-4">
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/shop" element={<Shop />} />
          <Route path="/product/:id" element={<ProductDetail />} />
          <Route path="/checkout" element={<Checkout />} />
        </Routes>
      </main>
    </Router>
  );
}

export default App;