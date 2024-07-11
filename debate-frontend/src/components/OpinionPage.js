import React, { useState } from 'react';

const OpinionPage = ({ debate, setOpinion }) => {
    const [opinion, setOpinionText] = useState('');

    const submitOpinion = () => {
        setOpinion(opinion);
    };

    return (
        <div>
            <h2>Debate Topic: {debate.topic}</h2>
            <textarea
                value={opinion}
                onChange={(e) => setOpinionText(e.target.value)}
                placeholder="Enter your opinion (150 words max)"
            />
            <button onClick={submitOpinion}>Submit Opinion</button>
        </div>
    );
};

export default OpinionPage;
