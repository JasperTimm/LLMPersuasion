import React, { useState } from 'react';
import '../styles/LikertScalePage.css';
import { axiosInstance } from '../config';
import InitialPositionDiagram from '../assets/images/initial_position.png';

const LikertScalePage = ({ debate, setDebate }) => {
    const [likertScore, setLikertScore] = useState(4);

    const likertLabels = [
        'Strongly Disagree',
        'Disagree',
        'Somewhat Disagree',
        'Neutral',
        'Somewhat Agree',
        'Agree',
        'Strongly Agree'
    ];

    const submitLikert = async () => {
        try {
            const response = await axiosInstance.post(`/initial_position`, {
                debate_id: debate.debate_id,
                initial_opinion: debate.initial_opinion,
                initial_likert_score: likertScore,
            });
            setDebate({
                ...debate,
                ...response.data,
                initial_likert_score: likertScore,
            });
        } catch (error) {
            console.error("Error updating position:", error);
        }
    };

    return (
        <div className="content-wrapper">
            <img src={InitialPositionDiagram} alt="Initial Position Diagram" className="flow-diagram" />
            <div className='container'>
                <h2 className="debate-title">Initial Position</h2>
                <h3>
                    Consider the debate topic above and rate your initial position on the scale below.
                </h3>
                <div className="range-container">
                    <input
                        type="range"
                        min="1"
                        max="7"
                        value={likertScore}
                        onChange={(e) => setLikertScore(Number(e.target.value))}
                    />
                </div>
                <div className="likert-labels">
                    {likertLabels.map((label, index) => (
                        <div
                            key={index}
                            className={`likert-label ${likertScore === index + 1 ? 'selected' : ''}`}
                            onClick={() => setLikertScore(index + 1)}
                        >
                            {label}
                        </div>
                    ))}
                </div>
                <button className='submit-button' onClick={submitLikert}>Submit</button>
            </div>
        </div>
    );
};

export default LikertScalePage;
