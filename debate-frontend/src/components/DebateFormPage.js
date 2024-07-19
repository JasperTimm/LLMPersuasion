import React from 'react';
import DebateHistory from './DebateHistory';
import DebateInput from './DebateInput';

const DebateFormPage = ({ debate, history, updateDebate }) => {

    const continueToFinalOpinion = () => {
        // Set debate state to 'final_opinion'
        updateDebate({ state: 'final_opinion' });
    };

    return (
        <div>
            <h2>Debate Topic: {debate.topic}</h2>
            <h3>You are arguing: {debate.user_side}</h3>
            <DebateHistory history={history} />
            {debate.state !== 'finished' ? (
                <DebateInput debateId={debate.debate_id} updateDebate={updateDebate} />
            ) : (
                <button onClick={continueToFinalOpinion}>Continue</button>
            )}
        </div>
    );
};

export default DebateFormPage;
