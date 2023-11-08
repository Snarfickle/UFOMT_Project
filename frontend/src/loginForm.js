import React, { useState, useSyncExternalStore } from 'react';
import { Container, Form, Button, Row, Col, Alert, Spinner } from 'react-bootstrap';
import { useAuth } from './AuthContext';
import { useNavigate } from 'react-router-dom';
import { backendURL } from './IPaddress';

function LoginPage() {
    const [username, setUserNameForm] = useState('');
    const [password, setPassword] = useState('');
    const [loginFailed, setLoginFailed] = useState(false);
    const [isLoading, setIsLoading] = useState(false);
    const { setToken, setUserName } = useAuth();
    const navigate = useNavigate();

    const handleUserNameChange = (e) => {
        const value = e.target.value;
        setUserNameForm(value);
    };

    const handlePasswordChange = (e) => {
        const value = e.target.value;
        setPassword(value);
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        setIsLoading(true);
        
        try {
            const response = await fetch(`${backendURL}/api/login/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                },
                body: `username=${username}&password=${encodeURIComponent(password)}`,
            });
            // const text = await response.text();
            // console.log("Fetching from:", `${backendURL}/api/login/`);
            // console.log("REACT_APP_HOST:", process.env.REACT_APP_HOST);
            // console.log("react environment:", process.env);


            
            const data = await response.json();
            // console.log("data: ", data);
            
            if (response.ok) {
                // console.log('Login successful:', data);
                setToken(data.access_token);
                setUserName(username);
                setUserNameForm('');
                setPassword('');
                setLoginFailed(false);
                try{
                    
                    const userResponse = await fetch(`${backendURL}/api/app-users/username/${username}`,
                    {
                        method: 'GET',
                        headers: {
                            'Content-Type': 'application/json',
                            'Authorization': `Bearer ${data.access_token}`
                        },
                    });
                    const userData = await userResponse.json();
                    setUserName(userData.first_name);
                } catch (error) {
                    console.log('User data fetching failed:', error);
                }

                navigate('/main');  // Navigate to MainPage
            } else {
                setUserNameForm('');
                setPassword('');
                setLoginFailed(true);
                // console.log('Login failed:', data);
            }
        } catch (error) {
            console.log('Error:', error);
            // console.log("Fetching from:", `${backendURL}/api/login/`);
            // console.log("REACT_APP_HOST:", process.env.REACT_APP_HOST);
            // console.log("react environment:", process.env);
            // Handle error, e.g., show error message to user
        } finally {
            setIsLoading(false);
        }}


    return (
        <Container fluid className="vh-100 d-flex align-items-center justify-content-center mt-3">
            <Row>
                <Col md={10} className='mt-3'>
                    <Form onSubmit={handleSubmit}>
                        <h3 className="mb-3">UFOMT Staff Login</h3>
                        {loginFailed && 
                            <Alert variant="danger" onClose={() => setLoginFailed(false)} dismissible>
                                Login failed. Please check your username and password.
                            </Alert>
                        }
                        <Form.Group controlId="username" className='mt-3'>
                            <Form.Label>Username</Form.Label>
                            <Form.Control 
                                type="text"
                                name="username"
                                value={username}
                                onChange={handleUserNameChange}
                                placeholder="Enter username"
                                required
                            />
                        </Form.Group>

                        <Form.Group controlId="password" className='mt-3'>
                            <Form.Label>Password</Form.Label>
                            <Form.Control 
                                type="password"
                                name="password"
                                value={password}
                                onChange={handlePasswordChange}
                                placeholder="Password"
                                required
                            />
                        </Form.Group>
                        
                        <Button variant="primary" className='mt-3' type="submit" disabled={isLoading}>
                            {isLoading ? (
                                <>
                                    <Spinner
                                        as="span"
                                        animation="border"
                                        size="sm"
                                        role="status"
                                        aria-hidden="true"
                                    />
                                    {' '}Loading...
                                </>
                            ) : 'Login'}
                        </Button>
                    </Form>
                </Col>
            </Row>
        </Container>
    );
}

export default LoginPage;
