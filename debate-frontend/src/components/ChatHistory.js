import React, { useEffect, useRef } from 'react';

const ChatHistory = ({ chatHistory }) => {
    const historyRef = useRef(null);
    const agentOrder = ['personalised agent', 'stats agent', 'executive agent'];

    useEffect(() => {
        if (historyRef.current) {
            historyRef.current.scrollTop = historyRef.current.scrollHeight;
        }
    }, [chatHistory]);

    return (
        <div ref={historyRef} className="chat-history-container">
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