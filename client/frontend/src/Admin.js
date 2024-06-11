import React, { useState, useEffect } from 'react';
import { Container, Row, Col, Card, Button, Alert } from 'react-bootstrap';
import axios from 'axios';

function Admin() {
    const [users, setUsers] = useState([]);
    const [message, setMessage] = useState('');

    useEffect(() => {
        const fetchUsers = async () => {
            try {
                const response = await axios({
                    method: 'get',
                    url: `${process.env.REACT_APP_API_URL}/users`,
                    withCredentials: false,
                });
                const usersData = response.data.users;
                setUsers(usersData);
            } catch (error) {
                console.error('Error fetching users:', error);
                setMessage('Error fetching users: ' + (error.response ? error.response.data : error.message));
            }
        };

        fetchUsers();
    }, []);

    const handleApproval = async (userId, approve) => {
        try {
            const response = await axios({
                method: 'patch',
                url: `${process.env.REACT_APP_API_URL}/users`,
                withCredentials: false,
                data:{
                    user_id: userId,
                    approved: approve
                }
            });
            setMessage(response.data.message);
            setUsers((prevUsers) =>
                prevUsers.map((user) =>
                    user._id.$oid === userId ? { ...user, approved_human: approve } : user
                )
            );
            window.location.reload();
        } catch (error) {
            console.error('Error updating user approval:', error);
            setMessage('Error updating user approval: ' + (error.response ? error.response.data : error.message));
        }
    };

    return (
        <Container className="mt-5">
            <Row className="justify-content-md-center">
                <Col md="8">
                    <h2>Admin Panel</h2>
                    {message && <Alert variant="info">{message}</Alert>}
                    {users.length === 0 ? (
                        <p>Loading...</p>
                    ) : (
                        users.map((user, i) => (
                            <Card key={i} className="mb-3">
                                <Card.Body>
                                    <Card.Title>Username: {user.username}</Card.Title>
                                    <Card.Text>
                                        <strong>AI Approved:</strong> {user.approved_ai ? 'Yes' : 'No'}
                                    </Card.Text>
                                    <Card.Text>
                                        <strong>Human Approved:</strong> {user.approved_human === null ? 'Pending' : user.approved_human ? 'Yes' : 'No'}
                                    </Card.Text>
                                    {user.approved_human === null ? (
                                        <div>
                                            <Button variant="success" onClick={() => handleApproval(user._id, true)} className="me-2">
                                                Approve
                                            </Button>
                                            <Button variant="danger" onClick={() => handleApproval(user._id, false)}>
                                                Reject
                                            </Button>
                                        </div>
                                    ) : (
                                        <p>The user has been reviewed.</p>
                                    )}
                                </Card.Body>
                            </Card>
                        ))
                    )}
                </Col>
            </Row>
        </Container>
    );
}

export default Admin;
