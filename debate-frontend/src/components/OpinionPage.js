import React, { useState } from 'react';
import '../styles/OpinionPage.css';
import IntialOpinionDiagram from '../assets/images/initial_opinion.png';

const OpinionPage = ({ debate, setDebate }) => {
    const [opinion, setOpinionText] = useState('');

    const submitOpinion = () => {
        setDebate({ ...debate, initial_opinion: opinion });
    };

    return (
      <div className="opinion-page">
        <div className="content-wrapper">
          <img src={IntialOpinionDiagram} alt="Initial Opinion Diagram" className="flow-diagram" />
          <div className='container'>
            <h2 className="debate-title">Initial Opinion</h2>
            <h3>
              Consider the debate topic above and share your initial opinion.
              Just one or two sentences to summarize your stance.
            </h3>
            <textarea
              className="input-textarea"
              value={opinion}
              onChange={(e) => setOpinionText(e.target.value)}
              placeholder="Briefly summarize your opinion on this topic in 1-2 sentences"
            />
            <button className="submit-button" onClick={submitOpinion}>
              Submit Opinion
            </button>
          </div>
        </div>
      </div>
    );
};

export default OpinionPage;