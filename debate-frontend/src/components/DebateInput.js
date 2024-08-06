import React, { useState } from 'react';
import { axiosInstance } from '../config';

const DebateInput = ({ debateId, updateDebate }) => {
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

    return (
        <div>
            <textarea
                value={userMessage}
                onChange={(e) => setUserMessage(e.target.value)}
                placeholder="Enter your message..."
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