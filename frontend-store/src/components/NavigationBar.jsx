import { useState } from 'react';
import { Navbar, Nav, Container, Offcanvas, Button } from 'react-bootstrap';
import { useUser } from '../context/UserContext';
import { useCart } from '../context/CartContext';
import { login, logout } from '../api';

const NavigationBar = () => {
  const { user, refetch } = useUser();
  const { cartCount } = useCart();
  const [showOffcanvas, setShowOffcanvas] = useState(false);

  const handleLogout = async () => {
    await logout();
    refetch(); // triggers re-fetch of user (will be null)
    window.location.href = '/';
  };

  return (
    <>
      <Navbar bg="light" expand="lg" className="mb-4">
        <Container>
          <Navbar.Brand href="/">Limelight Store</Navbar.Brand>
          <Navbar.Toggle aria-label="Toggle navigation" onClick={() => setShowOffcanvas(true)} />
          <Navbar.Collapse className="d-none d-lg-block">
            <Nav className="ms-auto">
              <Nav.Link href="/shop">Shop</Nav.Link>
              <Nav.Link href="/cart">Cart ({cartCount})</Nav.Link>
              {user ? (
                <>
                  <Navbar.Text>Hello, {user.name}</Navbar.Text>
                  <Button variant="outline-danger" size="sm" onClick={handleLogout} className="ms-2">Logout</Button>
                </>
              ) : (
                <Button variant="primary" size="sm" onClick={login}>Login</Button>
              )}
            </Nav>
          </Navbar.Collapse>
        </Container>
      </Navbar>

      {/* Offcanvas for mobile */}
      <Offcanvas show={showOffcanvas} onHide={() => setShowOffcanvas(false)} placement="end">
        <Offcanvas.Header closeButton>
          <Offcanvas.Title>Menu</Offcanvas.Title>
        </Offcanvas.Header>
        <Offcanvas.Body>
          <Nav className="flex-column">
            <Nav.Link href="/shop" onClick={() => setShowOffcanvas(false)}>Shop</Nav.Link>
            <Nav.Link href="/cart" onClick={() => setShowOffcanvas(false)}>Cart ({cartCount})</Nav.Link>
            {user ? (
              <>
                <Navbar.Text>Hello, {user.name}</Navbar.Text>
                <Button variant="outline-danger" size="sm" onClick={handleLogout} className="mt-2">Logout</Button>
              </>
            ) : (
              <Button variant="primary" size="sm" onClick={login}>Login</Button>
            )}
          </Nav>
        </Offcanvas.Body>
      </Offcanvas>
    </>
  );
};

export default NavigationBar;