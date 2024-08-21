import React, { useEffect, useRef } from 'react';
import '../styles/DebateHistory.css';

const DebateHistory = ({ debateHistory }) => {
    const historyRef = useRef(null);

    useEffect(() => {
        if (historyRef.current) {
            historyRef.current.scrollTop = historyRef.current.scrollHeight;
        }
    }, [debateHistory]);

    return (
        <div ref={historyRef} className="debate-history-container">
            <h2>Debate History</h2>
            <ul className="debate-history-list">
                {debateHistory.map((entry, index) => (
                    <li key={index} className="debate-history-item">
                        <strong>{entry.role}:</strong> {entry.message}
                    </li>
                ))}
            </ul>
        </div>
    );
};

export default DebateHistory;