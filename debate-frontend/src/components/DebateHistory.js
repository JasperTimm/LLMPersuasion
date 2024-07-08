import React from 'react';

const DebateHistory = ({ history }) => {
    return (
        <div>
            <h2>Debate History</h2>
            <ul>
                {history.map((entry, index) => (
                    <li key={index}>
                        <strong>{entry.role}:</strong> {entry.message}
                    </li>
                ))}
            </ul>
        </div>
    );
};

export default DebateHistory;
