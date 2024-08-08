// export default App;
import React, { useState, useEffect } from 'react';
import HomePage from './components/HomePage';
import Login from './components/Login';
import UserInfoPage from './components/UserInfoPage';
import { axiosInstance } from './config';
import './App.css';

const App = () => {
    const [isAuthenticated, setIsAuthenticated] = useState(false);
    const [userInfoCompleted, setUserInfoCompleted] = useState(false);
    const [debate, setDebate] = useState(null);
    const [debateHistory, setDebateHistory] = useState([]);
    const [chatHistory, setChatHistory] = useState({});

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

    useEffect(() => {
        const checkUserInfo = async () => {
            try {
                const response = await axiosInstance.get(`/check_user_info`);
                setUserInfoCompleted(response.data.user_info_completed);
            } catch (error) {
                setUserInfoCompleted(false);
            }
        };

        if (isAuthenticated) {
            checkUserInfo();
        }
    }, [isAuthenticated]);

    const updateDebate = (data) => {
        setDebateHistory([...debateHistory, { role: 'User', message: data.user_message }, { role: 'AI', message: data.llm_response }]);
        // Only update chat history if it was included in the response
        if (data.chat_history) setChatHistory({ ...chatHistory, [debate.state]: data.chat_history });
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

    if (isAuthenticated && !userInfoCompleted) {
        return <UserInfoPage setUserInfoCompleted={setUserInfoCompleted} />;
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
