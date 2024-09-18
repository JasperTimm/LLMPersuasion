import React, { useState } from 'react';
import '../styles/LikertScalePage.css';
import { axiosInstance } from '../config';
import FinalPositionDiagram from '../assets/images/final_position.png';

const FinalLikertScalePage = ({ debate, setDebate, user, setUser }) => {
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
            const response = await axiosInstance.post(`/final_position`, {
                debate_id: debate.debate_id,
                final_opinion: debate.final_opinion,
                final_likert_score: likertScore,
            });
            
            if (response.data.user_finished) {
                setUser({
                    ...user,
                    finished: true,
                });
            } else {
                setDebate({
                    ...debate,
                    final_likert_score: likertScore,
                });
            }
        } catch (error) {
            console.error("Error updating position:", error);
        }
    };

    return (
        <div className="content-wrapper">
            <img src={FinalPositionDiagram} alt="Final Position Diagram" className="flow-diagram" />
            <div className='container'>
                <h2 className="debate-title">Final Position</h2>
                <h3>Rate your opinion on a scale of 1-7:</h3>
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
                <button className="submit-button" onClick={submitLikert}>Submit</button>
            </div>
        </div>
    );
};

export default FinalLikertScalePage;
