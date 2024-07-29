// export default App;
import React, { useState, useEffect } from 'react';
import HomePage from './components/HomePage';
import Login from './components/Login';
import UserInfoPage from './components/UserInfoPage'; // Import the UserInfoPage component
import { axiosInstance } from './config';

const App = () => {
    const [isAuthenticated, setIsAuthenticated] = useState(false);
    const [userInfoCompleted, setUserInfoCompleted] = useState(false);
    const [debate, setDebate] = useState(null);
    const [history, setHistory] = useState([]);

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
                setUserInfoCompleted(response.data.userInfoCompleted);
            } catch (error) {
                setUserInfoCompleted(false);
            }
        };

        if (isAuthenticated) {
            checkUserInfo();
        }
    }, [isAuthenticated]);

    const updateDebate = (data) => {
        setHistory([...history, { role: 'User', message: data.user_message }, { role: 'AI', message: data.llm_response }]);
        setDebate({ ...debate, state: data.state });
    };

    const resetDebate = () => {
        setDebate(null);
        setHistory([]);
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
            history={history}
            updateDebate={updateDebate}
            resetDebate={resetDebate}
        />
    );
};

export default App;
