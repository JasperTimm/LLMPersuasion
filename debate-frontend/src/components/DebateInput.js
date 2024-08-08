import React, { useState } from 'react';
import { axiosInstance } from '../config';
import '../styles/DebateInput.css';

const DebateInput = ({ debateId, updateDebate, debateState }) => {
    const [userMessage, setUserMessage] = useState('');
    const [loading, setLoading] = useState(false);

    const sendMessage = async () => {
        setLoading(true);
        try {
            const response = await axiosInstance.post(`update_debate`, {
                debate_id: debateId,
                user_message: userMessage,
            });
            updateDebate(response.data);
            setUserMessage('');
        } catch (error) {
            console.error("Error sending message:", error);
        } finally {
            setLoading(false);
        }
    };

    const getPlaceholderText = () => {
        switch (debateState) {
            case 'intro':
                return 'Please enter your Introduction in the debate';
            case 'rebuttal':
                return 'Please enter your Rebuttal in the debate';
            case 'conclusion':
                return 'Please enter your Conclusion in the debate';
            default:
                return 'Enter your message...';
        }
    };

    return (
        <div>
            <textarea
                className="large-textarea"
                value={userMessage}
                onChange={(e) => setUserMessage(e.target.value)}
                placeholder={getPlaceholderText()}
                disabled={loading}
            />
            <button onClick={sendMessage} disabled={loading}>
                {loading ? 'Sending...' : 'Send'}
            </button>
            {loading && <div className="loading-indicator">Loading...</div>}
        </div>
    );
};

export default DebateInput;