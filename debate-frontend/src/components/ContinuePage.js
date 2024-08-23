import React, { useState } from 'react';
import { axiosInstance } from '../config';
import '../styles/ContinuePage.css';

function ContinuePage({ startDebate, user, setUser, resetDebate }) {
    const [selectedOption, setSelectedOption] = useState(null);
    const [showContinueLaterMessage, setShowContinueLaterMessage] = useState(false);

    const finishStudy = async () => {
        try {
            await axiosInstance.post(`/finish`);
            setUser({ ...user, finished: true });
        } catch (error) {
            console.error('Error finishing participation:', error);
        }
    };

    const handleOptionChange = (e) => {
        setSelectedOption(e.target.value);
    };

    const handleSubmit = () => {
        resetDebate();
        switch (selectedOption) {
            case 'continueNow':
                startDebate();
                break;
            case 'continueLater':
                setShowContinueLaterMessage(true);
                break;
            case 'finishStudy':
                finishStudy();
                break;
            default:
                alert('Please select an option to proceed.');
        }
    };

    return (
        <>
        {showContinueLaterMessage ? (
            <div className="continue-later-message">
                <p>Thank you for your participation.</p>
                <p>It's important that you return to the site later to conclude the study.</p>
                <p>You can now leave this page by logging out in the top right.</p>
            </div>
        ) : (
            <div className="continue-container">
                <h2 className="continue-title">What would you like to do next?</h2>
                <p className="continue-description">Please select one of the options below and click submit to proceed.</p>

                <div className="continue-options">
                    <div className={`continue-option continue-now ${selectedOption === 'continueNow' ? 'selected' : ''}`} 
                        onClick={() => setSelectedOption('continueNow')}>
                        <input
                            type="radio"
                            id="continue-now"
                            name="continueOption"
                            value="continueNow"
                            checked={selectedOption === 'continueNow'}
                            onChange={handleOptionChange}
                        />
                        <label htmlFor="continue-now">
                            <span className="option-title">Continue to Next Debate:</span> Move directly to the next debate and keep the momentum going.
                        </label>
                    </div>
                    <div className={`continue-option continue-later ${selectedOption === 'continueLater' ? 'selected' : ''}`} 
                        onClick={() => setSelectedOption('continueLater')}>
                        <input
                            type="radio"
                            id="continue-later"
                            name="continueOption"
                            value="continueLater"
                            checked={selectedOption === 'continueLater'}
                            onChange={handleOptionChange}
                        />
                        <label htmlFor="continue-later">
                            <span className="option-title">Continue Later:</span> Take a break and come back later to continue. It's crucial you conclude your participation in the study at some point. If you think you might forget to come back, we recommend you conclude your participation now.
                        </label>
                    </div>
                    <div className={`continue-option conclude-study ${selectedOption === 'finishStudy' ? 'selected' : ''}`} 
                        onClick={() => setSelectedOption('finishStudy')}>
                        <input
                            type="radio"
                            id="conclude-study"
                            name="continueOption"
                            value="finishStudy"
                            checked={selectedOption === 'finishStudy'}
                            onChange={handleOptionChange}
                        />
                        <label htmlFor="conclude-study">
                            <span className="option-title">Conclude Participation:</span> End your participation in the study. You won't be able to participate in any further debates.
                        </label>
                    </div>
                </div>
                <button className="submit-button" onClick={handleSubmit}>Submit</button>            
            </div>
        )}
        </>
    );
}

export default ContinuePage;