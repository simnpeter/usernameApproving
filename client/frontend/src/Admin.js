import React, { useState, useEffect } from 'react';
import axios from 'axios';

function Admin() {
    const [users, setUsers] = useState([]);
    const [message, setMessage] = useState('');

    useEffect(() => {
        const fetchUsers = async () => {
            try {
                const response = await axios.get('http://localhost:5001/users');
                const usersData = response.data.users.map(user => JSON.parse(user));
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
            const response = await axios.patch(`http://localhost:5001/users/${userId}`, {
                approved_human: approve
            });
            setMessage(response.data.message);
            setUsers((prevUsers) =>
                prevUsers.map((user) =>
                    user._id.$oid === userId ? { ...user, approved_human: approve } : user
                )
            );
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
                    <div key={i}>
                        <p>{user.username}</p>
                        {!user.approved_human && (
                            <button onClick={() => handleApproval(user._id.$oid, true)}>Approve</button>
                        )}
                    </div>
                ))
            )}
        </div>
    );
}

export default Admin;
