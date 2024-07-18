import React, { useState } from 'react';

const FinalOpinionPage = ({ debate, setDebate }) => {
    const [opinion, setOpinionText] = useState('');

    const submitOpinion = () => {
        setDebate({ ...debate, final_opinion: opinion });
    };

    return (
        <div>
            <h2>Debate Topic: {debate.topic}</h2>
            <h3>Now that the debate is over, what is your final opinion on this topic?</h3>
            <textarea
                value={opinion}
                onChange={(e) => setOpinionText(e.target.value)}
                placeholder="Enter your final opinion on this topic in a few sentences"
            />
            <button onClick={submitOpinion}>Submit Opinion</button>
        </div>
    );
};

export default FinalOpinionPage;