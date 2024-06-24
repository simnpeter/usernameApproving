// src/Register.js
import React, { useState } from 'react';
import axios from 'axios';
import { Form, Button, Modal, Container, Row, Col } from 'react-bootstrap';
import { useNavigate} from 'react-router-dom';

function Register() {
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [message, setMessage] = useState('');
    const navigate = useNavigate();
    const [approvedAi, setApprovedAi] = useState(null);
    const [showModal, setShowModal] = useState(false);

    const handleSubmit = async (e) => {
        e.preventDefault();
        try {
            const response = await axios({
                method: 'post',
                url: `${process.env.REACT_APP_API_URL}/register`,
                withCredentials: false,
                data: {
                    username: username,
                    password: password
                }
              });
            if (response.data) {
                setMessage(response.data.message);
                setApprovedAi(response.data.approved_ai);
                setShowModal(true);

            setTimeout(() => {
                setShowModal(false);
                navigate('/login');
            }, 3000); // Redirect after 5 seconds
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

    const handleLoginRedirect = async (e) => {
        navigate('/login');
    };

    return (
                <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'center' , flexDirection: 'column', height: '100vh' }}>
                    <div style={{border: '1px solid black', padding: '18px 36px', borderRadius: 30}}>
                        <h2 style={{textAlign: 'center'}}>Register</h2>
                        <Form onSubmit={handleSubmit}>
                            <Form.Group controlId="formUsername" className="mb-3"  style={{width: '100%'}}>
                                <Form.Label>Username:</Form.Label>
                                <Form.Control
                                    type="text"
                                    value={username}
                                    onChange={(e) => setUsername(e.target.value)}
                                    required
                                />
                            </Form.Group>
                            <Form.Group controlId="formPassword" className="mb-3"  style={{width: '100%'}}>
                                <Form.Label>Password:</Form.Label>
                                <Form.Control
                                    type="password"
                                    value={password}
                                    onChange={(e) => setPassword(e.target.value)}
                                    required
                                />
                            </Form.Group>
                            <Button variant="primary" type="submit"  style={{width: '50%'}}>
                                Register
                            </Button>
                        </Form>
                        <Button variant="link" onClick={handleLoginRedirect}>
                            Already have an account? Login
                        </Button>
                        {message && <p className="mt-3">{message}</p>}
                        <Modal show={showModal} onHide={() => setShowModal(false)}>
                            <Modal.Header closeButton>
                                <Modal.Title>Registration Status</Modal.Title>
                            </Modal.Header>
                            <Modal.Body>
                                <p>Username {approvedAi ? 'has been approved by AI.' : 'has not been approved by AI.'}</p>
                            </Modal.Body>
                            <Modal.Footer>
                                <Button variant="secondary" onClick={() => setShowModal(false)}>
                                    Close
                                </Button>
                            </Modal.Footer>
                        </Modal>
                    </div>
                </div>
    );
}

export default Register;
