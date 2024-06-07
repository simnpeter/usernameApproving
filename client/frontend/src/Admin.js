import React, { useState, useEffect } from 'react';
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
        <div>
            <h2>Admin Panel</h2>
            {message && <p>{message}</p>}
            {users.length === 0 ? (
                <p>Loading...</p>
            ) : (
                users.map((user, i) => (
                    <div key={i} style={{ border: '1px solid #ccc', padding: '10px', marginBottom: '10px' }}>
                        <p><strong>Username:</strong> {user.username}</p>
                        <p><strong>AI Approved:</strong> {user.approved_ai ? 'Yes' : 'No'}</p>
                        <p><strong>Human Approved:</strong> {user.approved_human === null ? 'Pending' : user.approved_human ? 'Yes' : 'No'}</p>
                        {user.approved_human === null ? (
                            <div>
                                <button onClick={() => handleApproval(user._id, true)} style={{ marginRight: '10px' }}>Approve</button>
                                <button onClick={() => handleApproval(user._id, false)}>Reject</button>
                            </div>
                        ) : (
                            <p>The user has been reviewed.</p>
                        )}
                    </div>
                ))
            )}
        </div>
    );
}

export default Admin;
