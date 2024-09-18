import React, { useEffect, useState } from 'react';
import { axiosInstance } from '../config';
import '../styles/ArgumentPage.css';
import ArgumentDiagram from '../assets/images/argument.png';

const ArgumentPage = ({ debate, setDebate }) => {
    const [argument, setArgument] = useState('');

    useEffect(() => {
        const fetchArgument = async () => {
            try {
                const response = await axiosInstance.post(`/get_argument`, { debate_id: debate.debate_id } );
                setArgument(response.data.argument);
            } catch (error) {
                console.error("Error fetching argument:", error);
            }
        };

        fetchArgument();
    }, [debate.debate_id]);

    const continueToFinalOpinion = () => {
        setDebate({ ...debate, state: 'final_opinion' });
    };

    return (
        <div className="content-wrapper">
            <img src={ArgumentDiagram} alt="Argument Diagram" className="flow-diagram" />
            <div className='container'>
                <div className="argument-container">
                    <h2>Please read the following argument carefully:</h2>
                    <div className="argument-text">
                        {argument}
                    </div>
                </div>
                <button className="continue-button" onClick={continueToFinalOpinion}>Continue</button>
            </div>
        </div>
    );
};

export default ArgumentPage;