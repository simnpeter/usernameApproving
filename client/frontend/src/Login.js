// src/Register.js
import React, { useState } from 'react';
import axios from 'axios';
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
        <div>
            <h2>Login</h2>
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
                <button type="submit">Login</button>
            </form>
            <button onClick={handleRegisterRedirect}>Doesn't have an account? Register</button>
            {message && <p>{message}</p>}
        </div>
    );
}

export default Login;
