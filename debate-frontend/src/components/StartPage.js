import React from 'react';
import axios from 'axios';

const StartPage = ({ setDebate }) => {
    const startDebate = async () => {
        try {
            const response = await axios.post('http://127.0.0.1:5000/start_debate');
            setDebate(response.data);
        } catch (error) {
            console.error("Error starting debate:", error);
        }
    };

    return (
        <div>
            <button onClick={startDebate}>Start New Debate</button>
        </div>
    );
};

export default StartPage;
