import React, { useState } from 'react';
import '../styles/LikertScalePage.css'; // Adjust the path based on your project structure
import { axiosInstance } from '../config';

const LikertScalePage = ({ debate, opinion, setDebate }) => {
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
            const response = await axiosInstance.post(`/update_position`, {
                debate_id: debate.debate_id,
                user_initial_opinion: opinion,
                likert_score: likertScore,
            });
            setDebate({ ...debate, ...response.data });
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

export default LikertScalePage;
