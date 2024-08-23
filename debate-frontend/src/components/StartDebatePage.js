import React, { useState } from 'react';
import { axiosInstance } from '../config';
import '../styles/StartDebatePage.css';

const StartDebatePage = ({ startDebate }) => {
    return (
        <div className="container">
            <h2 className="debate-title">How the Debate Process Works</h2>
            <ul className="debate-steps">
                <li className="debate-step">
                    <strong className="debate-step-title">Express Your Opinion:</strong> 
                    Start by briefly sharing your thoughts on the topic. Just one or two sentences to summarize your stance.
                </li>
                <hr className="debate-step-separator" />
                <li className="debate-step">
                    <strong className="debate-step-title">Rate Your Agreement:</strong> 
                    Indicate how strongly you agree or disagree with the topic using a scale from "Strongly Disagree" to "Strongly Agree."
                </li>
                <hr className="debate-step-separator" />
                <li className="debate-step">
                    <strong className="debate-step-title">Debate the Topic:</strong> 
                    Engage in a structured debate with the LLM. You'll go through an Introduction phase, a Rebuttal phase, and a Conclusion phase to explore the topic in depth.
                </li>
                <hr className="debate-step-separator" />
                <li className="debate-step">
                    <strong className="debate-step-title">Final Opinion:</strong> 
                    After the debate, share your final thoughts on the topic in one or two sentences.
                </li>
                <hr className="debate-step-separator" />
                <li className="debate-step">
                    <strong className="debate-step-title">Rate Again:</strong> 
                    Reassess your agreement with the topic to see if your opinion has shifted after the debate.
                </li>
            </ul>
            <button className="debate-start-button" onClick={startDebate}>Start Debate</button>
        </div>
    );    
};

export default StartDebatePage;