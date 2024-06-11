// src/Register.js
import React, { useState } from 'react';
import axios from 'axios';
import { Form, Button, Container, Row, Col } from 'react-bootstrap';
import { useNavigate } from 'react-router-dom';

function Login() {
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [message, setMessage] = useState('');
    const navigate = useNavigate();

    const handleSubmit = async (e) => {
        e.preventDefault();
        try {
            const response =  await axios({
                method: 'post',
                url: `${process.env.REACT_APP_API_URL}/login`,
                withCredentials: false,
                data: {
                    username: username,
                    password: password
                }
              });
            if (response.data) {
                setMessage(response.data.message);
                console.log(response.data)
                if(response.data.user.is_admin){
                    navigate('/admin');
                }
                else{
                    navigate('/user')
                }
            } else {
                setMessage('Unexpected error occurred');
            }
        } catch (error) {
            console.error('Error:', error); // Debug log
            if (error.response && error.response.data) {
                setMessage('Error: ' + error.response.data.message);
            } else {
                setMessage('Error: ' + error.message);
            }
        }
    };

    const handleRegisterRedirect = async (e) => {
        navigate('/register');
    };

    return (
        <Container>
            <Row className="justify-content-md-center">
                <Col md="6">
                    <div className="mt-5">
                        <h2>Login</h2>
                        <Form onSubmit={handleSubmit}>
                            <Form.Group controlId="formUsername" className="mb-3">
                                <Form.Label>Username:</Form.Label>
                                <Form.Control
                                    type="text"
                                    value={username}
                                    onChange={(e) => setUsername(e.target.value)}
                                    required
                                />
                            </Form.Group>
                            <Form.Group controlId="formPassword" className="mb-3">
                                <Form.Label>Password:</Form.Label>
                                <Form.Control
                                    type="password"
                                    value={password}
                                    onChange={(e) => setPassword(e.target.value)}
                                    required
                                />
                            </Form.Group>
                            <Button variant="primary" type="submit">
                                Login
                            </Button>
                        </Form>
                        <Button variant="link" onClick={handleRegisterRedirect}>
                            Don't have an account? Register
                        </Button>
                        {message && <p className="mt-3">{message}</p>}
                    </div>
                </Col>
            </Row>
        </Container>
    );
}

export default Login;
