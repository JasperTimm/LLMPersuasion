import React from 'react';

const ChatHistory = ({ chatHistory }) => {
    const agentOrder = ['personalised agent', 'stats agent', 'executive agent'];

    return (
        <div>
            <h2>Chat History</h2>
            {Object.entries(chatHistory).map(([phase, messages], phaseIndex) => (
                <div key={phaseIndex}>
                    <h3>{phase || 'Introduction'}</h3>
                    <ul>
                        {agentOrder.map((agent) => (
                            messages[agent] && (
                                <li key={agent}>
                                    <strong>{agent}:</strong> {messages[agent]}
                                </li>
                            )
                        ))}
                    </ul>
                </div>
            ))}
        </div>
    );
};

export default ChatHistory;