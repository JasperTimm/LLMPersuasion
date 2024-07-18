import React, { useState } from 'react';

const OpinionPage = ({ debate, setDebate }) => {
    const [opinion, setOpinionText] = useState('');

    const submitOpinion = () => {
        setDebate({ ...debate, initial_opinion: opinion });
    };

    return (
        <div>
            <h2>Debate Topic: {debate.topic}</h2>
            <textarea
                value={opinion}
                onChange={(e) => setOpinionText(e.target.value)}
                placeholder="Enter your opinion on this topic in a few sentences"
            />
            <button onClick={submitOpinion}>Submit Opinion</button>
        </div>
    );
};

export default OpinionPage;