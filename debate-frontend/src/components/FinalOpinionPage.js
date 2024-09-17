import React, { useState } from 'react';

const FinalOpinionPage = ({ debate, setDebate }) => {
    const [opinion, setOpinionText] = useState('');

    const submitOpinion = () => {
        setDebate({ ...debate, final_opinion: opinion });
    };

    return (
        <div className='container'>
            <h2 className="debate-title">Final Opinion</h2>
            <h3>Now that the debate is over, what is your final opinion on this topic?</h3>
            <textarea
                className="input-textarea"
                value={opinion}
                onChange={(e) => setOpinionText(e.target.value)}
                placeholder="Briefly summarize your opinion on this topic in 1-2 sentences"
            />
            <button className="submit-button" onClick={submitOpinion}>Submit Opinion</button>
        </div>
    );
};

export default FinalOpinionPage;