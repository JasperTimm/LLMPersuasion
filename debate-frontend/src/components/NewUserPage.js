import React, { useState, useRef, useEffect } from 'react';
import { axiosInstance } from '../config';
import '../styles/NewUserPage.css';

const NewUserPage = ({ setNewUser }) => {
    const [isScrolledToBottom, setIsScrolledToBottom] = useState(false);
    const [isChecked, setIsChecked] = useState(false);
    const [responseMessage, setResponseMessage] = useState('');
    const [loginDetails, setLoginDetails] = useState({ username: '', password: '' });
    const [userCreated, setUserCreated] = useState(false);
    const consentRef = useRef(null);

    const handleScroll = () => {
        const { scrollTop, scrollHeight, clientHeight } = consentRef.current;
        if (scrollTop + clientHeight >= scrollHeight) {
            setIsScrolledToBottom(true);
        }
    };

    const handleSubmit = async () => {
        try {
            const response = await axiosInstance.post('/create_new_user');
            const { username, password } = response.data;
            setLoginDetails({ username, password });
            setUserCreated(true);
        } catch (error) {
            setResponseMessage('Failed to create a new user.');
        }
    };

    const handleReturnToLogin = () => {
        setNewUser(false);
    };    

    useEffect(() => {
        const consentElement = consentRef.current;
        consentElement.addEventListener('scroll', handleScroll);
        return () => {
            consentElement.removeEventListener('scroll', handleScroll);
        };
    }, []);

    if (userCreated) {
        return (
            <div className="container">
                <h1>User Created Successfully</h1>
                <p className="response-message">
                    User created successfully.<br /><br />
                    <strong>Username:</strong> {loginDetails.username}<br />
                    <strong>Password:</strong> {loginDetails.password}<br /><br />
                    Please make a note of your login details and return to the login page to sign in.
                </p>
                <button onClick={handleReturnToLogin}>Return to Login</button>
            </div>
        );
    }

    return (
        <div className="container">
            <h1>Welcome to the Debate Platform</h1>
            <p>Thank you for taking the time to participate in this study. Your input is invaluable to us.</p>
            <p>Here is an overview of the process:</p>
            <ol>
                <li>
                    <strong>Demographics and Personality:</strong> First, you will provide some basic demographic information and complete a personality assessment. This helps us understand the diverse perspectives of our participants.
                </li>
                <li>
                    <strong>Initial Opinions:</strong> You will then share your initial opinions on five different topics. These topics are designed to cover a range of current and relevant issues.
                </li>
                <li>
                    <strong>Debate with LLM:</strong> Next, you will engage in a debate with a Language Learning Model (LLM) on each of the five topics. The LLM will present arguments and counterarguments to challenge your viewpoints.
                </li>
                <li>
                    <strong>Updated Opinions:</strong> After the debate, you will have the opportunity to update your opinions based on the discussion. This helps us understand how the debate influenced your views.
                </li>
            </ol>
            <p>We appreciate your participation!</p>
            <div className="consent-container" ref={consentRef}>
                <p>
                    {/* Placeholder text for the consent form */}
                    Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.
                </p>
                <p>
                    Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.
                </p>
            </div>
            <div className="consent-actions">
                <label>
                    <input
                        type="checkbox"
                        disabled={!isScrolledToBottom}
                        checked={isChecked}
                        onChange={(e) => setIsChecked(e.target.checked)}
                    />
                    I agree to the above
                </label>
                <button
                    type="button"
                    disabled={!isChecked}
                    onClick={handleSubmit}
                >
                    Submit
                </button>
            </div>
            {responseMessage && <p>{responseMessage}</p>}
        </div>
    );
};

export default NewUserPage;