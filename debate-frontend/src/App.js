import React, { useState, useEffect } from 'react';
import MainPage from './components/MainPage';
import Login from './components/Login';
import UserInfoPage from './components/UserInfoPage';
import NewUserPage from './components/NewUserPage';
import Profile from './components/Profile';
import EndEarlyPage from './components/EndEarlyPage';
import ConclusionPage from './components/ConclusionPage';
import ResultsPage from './components/ResultsPage';
import { axiosInstance } from './config';
import InstructionPage from './components/InstructionPage';
import QuizPage from './components/QuizPage';

import './App.css';
const App = () => {
    const [userInfoCompleted, setUserInfoCompleted] = useState(false);
    const [newUser, setNewUser] = useState(false);
    const [debate, setDebate] = useState(null);
    const [user, setUser] = useState(null);
    const [debateHistory, setDebateHistory] = useState([]);
    const [chatHistory, setChatHistory] = useState({});
    const [endEarly, setEndEarly] = useState(false);
    const [errorStartDebate, setErrorStartDebate] = useState('');
    const [showInstructions, setShowInstructions] = useState(true);
    const [quizCompleted, setQuizCompleted] = useState(false);
    const handleBackToInstructions = () => {
        setShowInstructions(true);
        setQuizCompleted(false);
    };
    

    useEffect(() => {
        const checkAuth = async () => {
            try {
                const response = await axiosInstance.get(`/protected`);
                setUser(response.data.user);
            } catch (error) {
                setUser(null);
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

        if (user) {
            checkUserInfo();
        }
    }, [user]);

    const startDebate = async () => {
        try {
            const response = await axiosInstance.post(`/start_debate`);
            setDebate(response.data);
            setErrorStartDebate(''); // Clear any previous error message
        } catch (error) {
            console.error("Error starting debate:", error);
            setErrorStartDebate('There was an issue starting the debate. Please try logging out and back in again. If the issue persists, contact support.');
        }
    };

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
        setErrorStartDebate('');
    };
    const handleContinueFromInstructions = () => {
        setShowInstructions(false);
    };
    

    if (!user) {
        if (newUser) {
            return <NewUserPage setNewUser={setNewUser}/>;
        } else {
            return <Login setUser={setUser} setNewUser={setNewUser} />;
        }
    }

    return (

        <div>
        <Profile user={user} setUser={setUser} resetDebate={resetDebate} setEndEarly={setEndEarly} />
        {user.concluded ? (
            <ResultsPage />
        ) : user.finished ? (
            <ConclusionPage user={user} setUser={setUser} />
        ) : endEarly ? (
            <EndEarlyPage setEndEarly={setEndEarly} user={user} setUser={setUser} />
        ) : !userInfoCompleted ? (
            <UserInfoPage setUserInfoCompleted={setUserInfoCompleted} />
        ) : showInstructions ? (
            <InstructionPage onContinue={handleContinueFromInstructions} /> 
        ) : !quizCompleted ? (
            <QuizPage 
            setQuizCompleted={setQuizCompleted}
            onBackToInstructions={handleBackToInstructions}/>

        ) : (
            <MainPage
                debate={debate}
                startDebate={startDebate}
                setDebate={setDebate}
                debateHistory={debateHistory}
                chatHistory={chatHistory}
                updateDebate={updateDebate}
                user={user}
                setUser={setUser}
                resetDebate={resetDebate}
                errorStartDebate={errorStartDebate}
            />
        )}
    </div>
    );
};

export default App;
