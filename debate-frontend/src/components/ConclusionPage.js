import React, { useState } from 'react';
import { axiosInstance } from '../config';
import '../styles/NewUserPage.css';

function ConclusionPage({ user, setUser }) {
    const [isScrolledToBottom, setIsScrolledToBottom] = useState(false);
    const [isChecked, setIsChecked] = useState(false);

    const handleScroll = (e) => {
        const { scrollTop, scrollHeight, clientHeight } = e.target;
        if (scrollTop + clientHeight >= scrollHeight - 1) {
            setIsScrolledToBottom(true);
        }
    };

    const concludeStudy = async () => {
        try {
            await axiosInstance.post(`/conclude`);
            setUser({ ...user, concluded: true });
        } catch (error) {
            console.error("Error concluding study:", error);
        }
    };

    return (
        <div className="container">
            <h1>Thank You for Your Participation</h1>
            <div className="consent-container" onScroll={handleScroll}>
                <p>We appreciate your time and effort in participating in our study. Here are some details about the study:</p>
                <ul>
                    <li>Some statistics presented during the study may have been fabricated for research purposes.</li>
                    <li>Your demographics and personality traits were used to tailor arguments to be more convincing to you.</li>
                    <li>Please refrain from discussing the study with others until they have completed their participation.</li>
                </ul>
                <p>Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed ac purus sit amet nisl tincidunt tincidunt
                    eget ac tortor. Nullam nec nunc nec nunc tincidunt tincidunt. Nullam nec nunc nec nunc tincidunt
                    tincidunt. Nullam nec nunc nec nunc tincidunt tincidunt. Nullam nec nunc nec nunc tincidunt tincidunt.
                    Nullam nec nunc nec nunc tincidunt tincidunt. Nullam nec nunc nec nunc tincidunt tincidunt. Nullam nec
                    nunc nec nunc tincidunt tincidunt. Nullam nec nunc nec nunc tincidunt tincidunt. Nullam nec nunc nec
                    nunc tincidunt tincidunt. Nullam nec nunc nec nunc tincidunt tincidunt. Nullam nec nunc nec nunc
                    tincidunt tincidunt. Nullam nec nunc nec nunc tincidunt tincidunt. Nullam nec nunc nec nunc tincidunt
                    tincidunt. Nullam nec nunc nec nunc tincidunt tincidunt. Nullam nec nunc nec nunc tincidunt tincidunt.
                    Nullam nec nunc nec nunc tincidunt tincidunt. Nullam nec nunc nec nunc tincidunt tincidunt. Nullam nec
                    nunc nec nunc tincidunt tincidunt. Nullam nec nunc nec nunc tincidunt tincidunt. Nullam nec nunc nec
                </p>
                <p>Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed ac purus sit amet nisl tincidunt tincidunt
                    eget ac tortor. Nullam nec nunc nec nunc tincidunt tincidunt. Nullam nec nunc nec nunc tincidunt
                    tincidunt. Nullam nec nunc nec nunc tincidunt tincidunt. Nullam nec nunc nec nunc tincidunt tincidunt.
                    Nullam nec nunc nec nunc tincidunt tincidunt. Nullam nec nunc nec nunc tincidunt tincidunt. Nullam nec
                    nunc nec nunc tincidunt tincidunt. Nullam nec nunc nec nunc tincidunt tincidunt. Nullam nec nunc nec
                    nunc tincidunt tincidunt. Nullam nec nunc nec nunc tincidunt tincidunt. Nullam nec nunc nec nunc
                    tincidunt tincidunt. Nullam nec nunc nec nunc tincidunt tincidunt. Nullam nec nunc nec nunc tincidunt
                    tincidunt. Nullam nec nunc nec nunc tincidunt tincidunt. Nullam nec nunc nec nunc tincidunt tincidunt.
                    Nullam nec nunc nec nunc tincidunt tincidunt. Nullam nec nunc nec nunc tincidunt tincidunt. Nullam nec
                    nunc nec nunc tincidunt tincidunt. Nullam nec nunc nec nunc tincidunt tincidunt. Nullam nec nunc nec
                </p>
                <p>Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed ac purus sit amet nisl tincidunt tincidunt
                    eget ac tortor. Nullam nec nunc nec nunc tincidunt tincidunt. Nullam nec nunc nec nunc tincidunt
                    tincidunt. Nullam nec nunc nec nunc tincidunt tincidunt. Nullam nec nunc nec nunc tincidunt tincidunt.
                    Nullam nec nunc nec nunc tincidunt tincidunt. Nullam nec nunc nec nunc tincidunt tincidunt. Nullam nec
                    nunc nec nunc tincidunt tincidunt. Nullam nec nunc nec nunc tincidunt tincidunt. Nullam nec nunc nec
                    nunc tincidunt tincidunt. Nullam nec nunc nec nunc tincidunt tincidunt. Nullam nec nunc nec nunc
                    tincidunt tincidunt. Nullam nec nunc nec nunc tincidunt tincidunt. Nullam nec nunc nec nunc tincidunt
                    tincidunt. Nullam nec nunc nec nunc tincidunt tincidunt. Nullam nec nunc nec nunc tincidunt tincidunt.
                    Nullam nec nunc nec nunc tincidunt tincidunt. Nullam nec nunc nec nunc tincidunt tincidunt. Nullam nec
                    nunc nec nunc tincidunt tincidunt. Nullam nec nunc nec nunc tincidunt tincidunt. Nullam nec nunc nec
                </p>                                
            </div>
            <div className="consent-actions">
                <label className={isScrolledToBottom ? 'label-bold' : 'label-unbold'}>
                    <input
                        type="checkbox"
                        disabled={!isScrolledToBottom}
                        className={!isScrolledToBottom ? 'checkbox-disabled' : ''}
                        checked={isChecked}
                        onChange={(e) => setIsChecked(e.target.checked)}
                    />
                    I have read the above
                </label>
                <button
                    type="button"
                    disabled={!isChecked}
                    onClick={concludeStudy}
                >
                    Submit
                </button>
            </div>
        </div>
    );
}

export default ConclusionPage;