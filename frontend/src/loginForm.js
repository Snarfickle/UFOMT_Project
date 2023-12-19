import React, { useState } from 'react';
import { Container, Form, Button, Row, Col, Alert, Spinner } from 'react-bootstrap';
import { useAuth } from "./store/AuthContext";
import { useNavigate } from 'react-router-dom';
import { backendURL } from './IPaddress';

function LoginPage() {
    const [username, setUserNameForm] = useState('');
    const [password, setPassword] = useState('');
    const [loginFailed, setLoginFailed] = useState(false);
    const [isLoading, setIsLoading] = useState(false);
    const { login } = useAuth();
    const navigate = useNavigate();

    const handleUserNameChange = (e) => {
        setUserNameForm(e.target.value);
    };

    const handlePasswordChange = (e) => {
        setPassword(e.target.value);
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        setIsLoading(true);

        try {
            await login(username, password);
        } catch (error) {
            console.error('Login Error:', error);
            setLoginFailed(true);
        } finally {
            setIsLoading(false);
            setUserNameForm('');
            setPassword('');
        }
    };

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
