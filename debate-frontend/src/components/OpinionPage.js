import React, { useState } from 'react';
import '../styles/OpinionPage.css';

const OpinionPage = ({ debate, setDebate }) => {
    const [opinion, setOpinionText] = useState('');

    const submitOpinion = () => {
        setDebate({ ...debate, initial_opinion: opinion });
    };

    return (
      <div className='container'>
        <div className="debate-topic">
          <span className="debate-topic-label">Debate Topic:</span>
          <span>{debate.topic}</span>
        </div>
        <textarea
          className="input-textarea"
          value={opinion}
          onChange={(e) => setOpinionText(e.target.value)}
          placeholder="Enter your opinion on this topic in a few sentences"
        />
        <button className="submit-button" onClick={submitOpinion}>
          Submit Opinion
        </button>
      </div>
    );
};

export default OpinionPage;