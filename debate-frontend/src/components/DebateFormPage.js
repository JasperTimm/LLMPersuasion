import React from 'react';
import DebateHistory from './DebateHistory';
import DebateInput from './DebateInput';
import axios from 'axios';

const DebateFormPage = ({ debate, history, updateDebate, resetDebate }) => {
    const startNewDebate = async () => {
        try {
            const response = await axios.post('http://127.0.0.1:5000/start_debate');
            // When setDebate runs with the new debate data, 
            // the App component will re-render with the new debate
            // as the opinion state will be reset to an empty string
            resetDebate(response.data);
        } catch (error) {
            console.error("Error starting new debate:", error);
        }
    };

    return (
        <div>
            <h2>Debate Topic: {debate.topic}</h2>
            <h3>You are arguing: {debate.user_side}</h3>
            <DebateHistory history={history} />
            {debate.state !== 'finished' ? (
                <DebateInput debateId={debate.debate_id} updateDebate={updateDebate} />
            ) : (
                <button onClick={startNewDebate}>Start New Debate</button>
            )}
        </div>
    );
};

export default DebateFormPage;
