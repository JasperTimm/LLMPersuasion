import React, { useState, useRef, useEffect } from 'react';
import { axiosInstance } from '../config';
import '../styles/NewUserPage.css';

const NewUserPage = ({ setNewUser }) => {
    const [isScrolledToBottom, setIsScrolledToBottom] = useState(false);
    const [isChecked, setIsChecked] = useState(false);
    const [responseMessage, setResponseMessage] = useState('');
    const [loginDetails, setLoginDetails] = useState({ username: '', password: '' });
    const [userCreated, setUserCreated] = useState(false);
    const consentContainerRef = useRef(null);
    const [isServiceParticipant, setIsServiceParticipant] = useState(false);
    const [participantId, setParticipantId] = useState('');
    const [service, setService] = useState('');

    const handleParticipantTypeChange = (event) => {
        setIsServiceParticipant(event.target.value === 'service');
    };

    const handleParticipantIdChange = (event) => {
        setParticipantId(event.target.value);
    };

    const handleServiceChange = (event) => {
        setService(event.target.value);
    };

    useEffect(() => {
        const handleScroll = () => {
            const container = consentContainerRef.current;
            if (container.scrollHeight - container.scrollTop <= container.clientHeight + 1) {
                setIsScrolledToBottom(true);
            }
        };

        const container = consentContainerRef.current;
        container.addEventListener('scroll', handleScroll);

        return () => {
            container.removeEventListener('scroll', handleScroll);
        };
    }, []);

    const handleSubmit = async () => {
        try {
            const response = isServiceParticipant ? 
                await axiosInstance.post('/create_new_user', { participantId, service }) : 
                await axiosInstance.post('/create_new_user', {});
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
            <p>Thank you for taking the time to participate in this study. Your input is invaluable to us and we appreciate your participation!</p>
            <div className='participant-info'>
                <p>Are you a volunteer or a paid participant?</p>
                <label>
                    <input
                        type="radio"
                        value="volunteer"
                        checked={!isServiceParticipant}
                        onChange={handleParticipantTypeChange}
                    />
                    Volunteer
                </label>
                <label>
                    <input
                        type="radio"
                        value="service"
                        checked={isServiceParticipant}
                        onChange={handleParticipantTypeChange}
                    />
                    Paid Participant
                </label>
                {isServiceParticipant && (
                    <div>
                        <br />
                        <label>
                            Participant ID:
                            <input
                                type="text"
                                value={participantId}
                                onChange={handleParticipantIdChange}
                            />
                        </label>
                        <label>
                            Service:
                            <select value={service} onChange={handleServiceChange}>
                                <option value="">Select a service</option>
                                <option value="prolific">Prolific</option>
                                <option value="amazon">Amazon Mechanical Turk</option>
                            </select>
                        </label>
                    </div>
                )}
            </div>
            <p>Please read the consent form below and confirm your agreement to proceed.</p>
            <div className="consent-container" ref={consentContainerRef}>
                <h1>Consent Form</h1>

                <h2>1. Title of Research</h2>
                <p>
                    You are being invited to take part in the research study titled “Opinion Changes Based on Debating Large Language Models.” Before deciding to participate, it is important that you understand certain details of the study. Please take the time to read the following information carefully. If you have any questions or require further information, you can contact us using the details provided in the “Withdrawal of Consent” section below.
                </p>

                <h2>2. Project Description and Aim of the Study</h2>
                <p>
                    The purpose of this project is to explore whether interacting with a Large Language Model (LLM) in a debate format can influence individuals' opinions on various topics. Human participants will be presented with a specific topic and asked to state their opinion before and after engaging in a debate with the LLM. This study aims to investigate the potential of LLMs to affect human opinion.
                </p>

                <h2>3. Data Controller, Research Group, and Principal Investigator</h2>
                <p><strong>Principal Investigator:</strong> Jasper Timm</p>
                <p><strong>Data Controller:</strong> Jasper Timm</p>
                <p><strong>Other Researchers:</strong> Chetan Talele</p>

                <h2>4. Study Procedure</h2>
                <p>
                    If you agree to participate in this study, your consent will lead to the following procedures:
                </p>
                <ul>
                    <li>Upon submitting your consent, a new user account will be generated for you, containing a randomly assigned user ID and password. This account will allow you to log in to the debate website.</li>
                    <li>During your first login, you will be asked to complete a series of questions regarding your demographics (e.g., age, gender, profession) and personality traits (e.g., introversion, extroversion).</li>
                    <li>You will then be presented with a topic and asked to express your opinion in one or two sentences. Additionally, you will indicate how strongly you agree or disagree with the topic.</li>
                    <li>The study will then proceed with a debate between you and the LLM. The debate will consist of three phases: Introduction, Rebuttal, and Conclusion. You will begin each phase and alternate turns with the LLM.</li>
                    <li>In some cases, instead of engaging in a debate, you will be presented with a pre-constructed argument.</li>
                    <li>After the debate, you will have the opportunity to revise your opinion and state whether you still agree or disagree with the topic.</li>
                    <li>Paid participants are required to complete four debates and read a passage to fulfill the study requirements.</li>
                    <li>Volunteers may choose to end their participation at any point before completing all debates. This can be done either at the end of a debate or by selecting the appropriate option from the Profile icon in the top right corner of the screen after logging in.</li>
                    <li>At the end of your participation, you will receive additional information about the study, including insights into your specific debates, for your interest and clarification. Paid participants will receive a completion code to receive compensation.</li>
                    <li>You are requested not to share the details of your participation with other participants who have not yet completed the study.</li>
                </ul>

                <h2>5. Benefits and Risks</h2>
                <p><strong>Risks:</strong></p>
                <ul>
                    <li>The topics selected for the debates are intended to be non-controversial, focusing primarily on new technologies. However, if a topic feels personal or sensitive, it could potentially be upsetting.</li>
                    <li>Large Language Models, while advanced, may occasionally produce hallucinated or incorrect information.</li>
                    <li>Participation in the study may result in a change in your opinion on certain topics.</li>
                </ul>
                <p><strong>Benefits:</strong></p>
                <ul>
                    <li>Upon completing your participation, you will have access to your debate logs and an analysis of your debates.</li>
                    <li>Your participation contributes to a body of research aimed at understanding the capabilities and impact of LLMs on human opinion.</li>
                </ul>

                <h2>6. Type of Personal Data and When It Is Deleted/Anonymized</h2>
                <p>
                    All data collected during the study will be securely stored in an encrypted database on a secure server. The types of data collected include demographic and personality information as previously mentioned.
                    Since user IDs are randomly generated, the data is fully anonymized, meaning there is no identifiable information connected to you.
                    The LLM model providers we use may receive anonymized data to improve their responses. However, these providers generally do not retain logs of these requests for longer than 30 days.
                    The data collected will be aggregated as part of the study and will not be linked to individual identities.
                </p>

                <h2>7. Withdrawal of Consent</h2>
                <p>
                    Participation in this study is entirely voluntary. You may withdraw your consent at any time without providing a reason by notifying the principal investigator, Jasper Timm, at jasper.timm@gmail.com.
                    If you wish to have your data removed from the study, you will need to provide the user ID you used during the study, as we have no other means of identifying your data.
                </p>

                <h2>8. User Agreement</h2>
                <p>By participating in this study, you agree to the following:</p>
                <ul>
                    <li>You will provide honest answers to all questions without feeling pressured into giving any specific response and will make your best effort to contribute meaningfully to the debate.</li>
                    <li>The responses you provide are your own and have not been aided by any AI or automated tools.</li>
                    <li>You will create only one user account for yourself.</li>
                    <li>You will not discuss the details of the study with other participants who have not yet completed their involvement.</li>
                    <li>You will not attempt to hack or manipulate the website to circumvent the standard user flow.</li>
                </ul>

                <h2>Signature</h2>
                <p>
                    By ticking the box below, you confirm that you have read and understood the above information and that:
                </p>
                <ul>
                    <li>Your participation is voluntary, and you may withdraw your consent and discontinue participation in the project at any time. Your refusal to participate will not result in any penalty.</li>
                    <li>By ticking this agreement, you do not waive any legal rights or release the researchers from liability for negligence.</li>
                    <li>You give your consent to participate as a subject in the study as described above.</li>
                    <li>You agree to the terms outlined in the User Agreement.</li>
                </ul>
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
                    I confirm and agree to the above
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