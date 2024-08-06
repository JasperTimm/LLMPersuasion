import React from 'react';

const DebateHistory = ({ debateHistory }) => {
    return (
        <div>
            <h2>Debate History</h2>
            <ul>
                {debateHistory.map((entry, index) => (
                    <li key={index}>
                        <strong>{entry.role}:</strong> {entry.message}
                    </li>
                ))}
            </ul>
        </div>
    );
};

export default DebateHistory;
