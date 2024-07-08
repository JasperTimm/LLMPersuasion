import React, { useState } from 'react';
import axios from 'axios';

const DebateForm = ({ setDebate }) => {
    const [userSide, setUserSide] = useState('FOR');

    const startDebate = async () => {
        try {
            const response = await axios.post('http://127.0.0.1:5000/create_debate', { user_side: userSide });
            setDebate(response.data);
        } catch (error) {
            console.error("Error starting debate:", error);
        }
    };

    return (
        <div>
            <h2>Start a New Debate</h2>
            <label>
                Choose your side:
                <select value={userSide} onChange={(e) => setUserSide(e.target.value)}>
                    <option value="FOR">FOR</option>
                    <option value="AGAINST">AGAINST</option>
                </select>
            </label>
            <button onClick={startDebate}>Start Debate</button>
        </div>
    );
};

export default DebateForm;
