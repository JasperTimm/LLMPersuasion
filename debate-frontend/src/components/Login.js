import React, { useState } from 'react';
import { axiosInstance } from '../config';
import '../styles/Login.css';

const Login = ({ setUser, setNewUser }) => {
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [errorMessage, setErrorMessage] = useState('');

    const handleSubmit = async (e) => {
        e.preventDefault();
        try {
            const response = await axiosInstance.post(`/login`, { username, password });
            setUser(response.data.user);
            setErrorMessage('');
        } catch (error) {
            setErrorMessage('Login failed');
        }
    };

    return (
        <form onSubmit={handleSubmit}>
            <div>
                <label>Username:</label>
                <input type="text" value={username} onChange={(e) => setUsername(e.target.value)} />
            </div>
            <div>
                <label>Password:</label>
                <input type="password" value={password} onChange={(e) => setPassword(e.target.value)} />
            </div>
            <button type="submit">Login</button>
            <div className="create-account-link">
                <button type="button" onClick={() => setNewUser(true)}>Create a new account</button>
            </div>
            {errorMessage && <div style={{ color: 'red' }}>{errorMessage}</div>}            
        </form>
    );
};

export default Login;