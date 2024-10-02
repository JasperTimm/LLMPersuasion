import React, { useState } from 'react';
import { axiosInstance } from '../config';
import '../styles/DebateInput.css';

const DebateInput = ({ debateId, updateDebate, debateState }) => {
    const [userMessage, setUserMessage] = useState('');
    const [loading, setLoading] = useState(false);
    const [wordCount, setWordCount] = useState(0);

    const sendMessage = async () => {
        setLoading(true);
        try {
            const response = await axiosInstance.post(`update_debate`, {
                debate_id: debateId,
                user_message: userMessage,
            });
            updateDebate(response.data);
            setUserMessage('');
            setWordCount(0);
        } catch (error) {
            console.error("Error sending message:", error);
        } finally {
            setLoading(false);
        }
    };

    const handleInputChange = (e) => {
        const message = e.target.value;
        setUserMessage(message);
        setWordCount(message.split(/\s+/).filter(word => word.length > 0).length);
    };

    const getWordCountMessage = () => {
        if (wordCount < 50) {
            return { text: 'Too short', color: 'red' };
        } else if (wordCount <= 100) {
            return { text: 'Not bad', color: 'orange' };
        } else if (wordCount <= 150) {
            return { text: 'Good', color: 'yellowgreen' };
        } else {
            return { text: 'Great', color: 'green' };
        }
    };

    const wordCountMessage = getWordCountMessage();

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
        <div className="debate-input-container">
            <textarea
                className="large-textarea"
                value={userMessage}
                onChange={handleInputChange}
                placeholder={getPlaceholderText()}
                disabled={loading}
            />
            <div className="action-container">
                <div className="word-count" style={{ color: wordCountMessage.color }}>
                    Word Count: {wordCount} - {wordCountMessage.text}
                </div>
                <button onClick={sendMessage} disabled={loading || wordCount < 50}>
                    {loading ? 'Sending...' : 'Send'}
                </button>
            </div>
            {loading && <div className="loading-indicator">Loading...</div>}
        </div>
    );
};

export default DebateInput;