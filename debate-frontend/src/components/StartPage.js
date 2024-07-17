import React from 'react';
import { axiosInstance } from '../config';

const StartPage = ({ setDebate }) => {
    const startDebate = async () => {
        try {
            const response = await axiosInstance.post(`/start_debate`);
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
