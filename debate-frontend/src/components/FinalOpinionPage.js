import React, { useState } from 'react';

const FinalOpinionPage = ({ debate, setDebate }) => {
    const [opinion, setOpinionText] = useState('');

    const submitOpinion = () => {
        setDebate({ ...debate, final_opinion: opinion });
    };

    return (
        <div className='container'>
            <div className="debate-topic">
                <span className="debate-topic-label">Debate Topic:</span>
                <span>{debate.topic}</span>
            </div>
            <h3>Now that the debate is over, what is your final opinion on this topic?</h3>
            <textarea
                className="input-textarea"
                value={opinion}
                onChange={(e) => setOpinionText(e.target.value)}
                placeholder="Enter your final opinion on this topic in a few sentences"
            />
            <button className="submit-button" onClick={submitOpinion}>Submit Opinion</button>
        </div>
    );
};

export default FinalOpinionPage;