import React from 'react';
import { Navbar, Button, Nav } from 'react-bootstrap';
import { useAuth } from './AuthContext';
import { useNavigate, NavLink } from 'react-router-dom';

function NavbarComponent() {
    const { setToken, setUserName } = useAuth();
    const navigate = useNavigate();

    const handleLogout = () => {
        // Clear authentication data
        setToken(null);
        setUserName(null);
        
        // Redirect to login page
        navigate('/login');
    };

    return (
        <Navbar bg="light" expand="lg">
            <Navbar.Brand href="#home">UFOMT</Navbar.Brand>
            <Navbar.Toggle aria-controls="basic-navbar-nav" />
            <Navbar.Collapse id="basic-navbar-nav" className="justify-content-end">
                <Nav>
                    <NavLink 
                        to="/formsubmission" 
                        className="nav-link" 
                        activeclassname="active"
                    >
                        Form Submission
                    </NavLink>
                </Nav>
                <Button variant="outline-dark" onClick={handleLogout}>Logout</Button>
            </Navbar.Collapse>
        </Navbar>
    );
}

export default NavbarComponent;
