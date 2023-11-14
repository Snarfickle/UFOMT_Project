import React, {useEffect, useState} from "react";
import { Container, Button, Fade, Form, Alert } from "react-bootstrap";
import { useAuth, useUserData } from "./store/AuthContext";
import { useNavigate } from "react-router-dom";
import './CSS/MainPage.css';
import NavbarComponent from './Nav';
import { backendURL } from "./IPaddress";

function MainPage() {
    const [show, setShow] = useState(true);
    const {userData } = useUserData();
    const navigate = useNavigate();
    const {authState} = useAuth();
       

    useEffect(() => {
        const timer = setTimeout(() => {
            setShow(false);
        }, 3000);
    },[]);
    useEffect(() => {
        if (!authState) {
            navigate('/login');
        }
        // Dependency array includes authState to react to its changes
    }, [authState, navigate]);


    return (    
<div>
    {authState && (
    <div>
    <NavbarComponent/>

    <Container className="vh-100 d-flex align-items-center justify-content-center">
        
        {/* Greeting Section */}
        <Fade in={show} timeout={4000}>
            <h1>Hello, {userData ? userData.first_name : 'Loading...'}!</h1>
        </Fade>

    </Container>
    </div>)};
    </div>
    );
}

export default MainPage;
