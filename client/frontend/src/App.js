// src/App.js
import React from 'react';
import { BrowserRouter as Router, Route, Routes, Navigate } from 'react-router-dom';
import Register from './Register';
import Login from './Login';
import Admin from './Admin'
import User from './User'
import './App.css';

function App() {
    return (
        <Router>
            <Routes>
                <Route path="/" element={<Navigate to="/register" />} />
                <Route path="/register" element={<Register />} />
                <Route path="/login" element={<Login />} />
                <Route path="/admin" element={<Admin />} />
                <Route path="/user" element={<User />} />
            </Routes>
        </Router>
    );
}

export default App;
