import React, { useState } from 'react';
import '../styles/LikertScalePage.css';
import { axiosInstance } from '../config';

const FinalLikertScalePage = ({ debate, resetDebate }) => {
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
            // We actually don't need the response here as 
            // we're just resetting the debate
            const response = await axiosInstance.post(`/final_position`, {
                debate_id: debate.debate_id,
                final_opinion: debate.final_opinion,
                final_likert_score: likertScore,
            });

            resetDebate();
        } catch (error) {
            console.error("Error updating position:", error);
        }
    };

    return (
        <div>
            <h2>Debate Topic: {debate.topic}</h2>
            <p>Rate your opinion on a scale of 1-7:</p>
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
            <button onClick={submitLikert}>Submit</button>
        </div>
    );
};

export default FinalLikertScalePage;
