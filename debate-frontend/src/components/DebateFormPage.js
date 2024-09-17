import React from 'react';
import DebateHistory from './DebateHistory';
import DebateInput from './DebateInput';
import ChatHistory from './ChatHistory';
import '../styles/DebateFormPage.css';

const DebateFormPage = ({ debate, debateHistory, chatHistory, updateDebate }) => {

    const continueToFinalOpinion = () => {
        updateDebate({ state: 'final_opinion' });
    };

    return (
        <div>
            <div className="debate-info">
                <h3 className="debate-side">You are arguing: <i>{debate.user_side}</i></h3>
                <h3 className="debate-initial-opinion"><strong>Your initial opinion:</strong> {debate.initial_opinion}</h3>
            </div>
            {Object.keys(debateHistory).length > 0 ? (
                <div className="history-container">
                    <div className={`debate-history ${Object.keys(chatHistory).length > 0 ? 'with-chat' : ''}`}>
                        <DebateHistory debateHistory={debateHistory} />
                    </div>
                    {Object.keys(chatHistory).length > 0 && (
                        <div className="chat-history">
                            <ChatHistory chatHistory={chatHistory} />
                        </div>
                    )}
                </div>
            ) : null}
            <div className="input-container">
                {debate.state !== 'finished' ? (
                    <DebateInput debateId={debate.debate_id} updateDebate={updateDebate} debateState={debate.state} />
                ) : (
                    <button onClick={continueToFinalOpinion}>Continue</button>
                )}
            </div>
        </div>
    );
};

export default DebateFormPage;