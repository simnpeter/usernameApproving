// src/Register.js
import React, { useState } from 'react';
import axios from 'axios';
import { Modal, Button } from 'react-bootstrap';
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
            }, 5000); // Redirect after 5 seconds
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
        <div>
            <h2>Register</h2>
            <form onSubmit={handleSubmit}>
                <div>
                    <label>Username:</label>
                    <input
                        type="text"
                        value={username}
                        onChange={(e) => setUsername(e.target.value)}
                        required
                    />
                </div>
                <div>
                    <label>Password:</label>
                    <input
                        type="password"
                        value={password}
                        onChange={(e) => setPassword(e.target.value)}
                        required
                    />
                </div>
                <button type="submit">Register</button>
            </form>
            <button onClick={handleLoginRedirect}>Already have an account? Login</button>
            {message && <p>{message}</p>}
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
    );
}

export default Register;
