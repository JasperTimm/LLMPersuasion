import React, { useState } from 'react';
import axios from 'axios';

const DebateInput = ({ debateId, updateDebate }) => {
    const [userMessage, setUserMessage] = useState('');

    const sendMessage = async () => {
        try {
            const response = await axios.post('http://127.0.0.1:5000/update_debate', {
                debate_id: debateId,
                user_message: userMessage,
            });
            updateDebate(response.data);
            setUserMessage('');
        } catch (error) {
            console.error("Error sending message:", error);
        }
    };

    return (
        <div>
            <textarea
                value={userMessage}
                onChange={(e) => setUserMessage(e.target.value)}
                placeholder="Enter your message..."
            />
            <button onClick={sendMessage}>Send</button>
        </div>
    );
};

export default DebateInput;
