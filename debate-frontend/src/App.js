import React, { useState, useEffect } from 'react';
import HomePage from './components/HomePage';
import Login from './components/Login';
import { axiosInstance } from './config';

const App = () => {
    const [isAuthenticated, setIsAuthenticated] = useState(false);
    const [debate, setDebate] = useState(null);
    const [debateHistory, setDebateHistory] = useState([]);
    const [chatHistory, setChatHistory] = useState([]);

    useEffect(() => {
        const checkAuth = async () => {
            try {
                await axiosInstance.get(`/protected`);
                setIsAuthenticated(true);
            } catch (error) {
                setIsAuthenticated(false);
            }
        };
        checkAuth();
    }, []);

    const updateDebate = (data) => {
        setDebateHistory([...debateHistory, { role: 'User', message: data.user_message }, { role: 'AI', message: data.llm_response }]);
        setChatHistory({ ...chatHistory, [debate.state]: data.chat_history });
        setDebate({ ...debate, state: data.state });
    };

    const resetDebate = () => {
        setDebate(null);
        setDebateHistory([]);
        setChatHistory([]);
    };

    if (!isAuthenticated) {
        return <Login setIsAuthenticated={setIsAuthenticated} />;
    }

    return (
        <HomePage
            debate={debate}
            setDebate={setDebate}
            debateHistory={debateHistory}
            chatHistory={chatHistory}
            updateDebate={updateDebate}
            resetDebate={resetDebate}
        />
    );
};

export default App;