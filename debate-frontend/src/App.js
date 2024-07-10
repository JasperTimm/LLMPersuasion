import React, { useState } from 'react';
import StartPage from './components/StartPage';
import OpinionPage from './components/OpinionPage';
import LikertScalePage from './components/LikertScalePage';
import DebateFormPage from './components/DebateFormPage';

const App = () => {
    const [debate, setDebate] = useState(null);
    const [opinion, setOpinion] = useState('');
    const [history, setHistory] = useState([]);

    const updateDebate = (data) => {
        setHistory([...history, { role: 'User', message: data.user_message }, { role: 'AI', message: data.llm_response }]);
        setDebate({ ...debate, state: data.state });
    };

    const resetDebate = () => {
        setDebate(null);
        setOpinion('');
        setHistory([]);
    };

    return (
        <div>
            <h1>Debate Platform</h1>
            {!debate ? (
                <StartPage setDebate={setDebate} />
            ) : !opinion ? (
                <OpinionPage debate={debate} setOpinion={setOpinion} />
            ) : debate.user_side ? (
                <DebateFormPage debate={debate} history={history} updateDebate={updateDebate} resetDebate={resetDebate} />
            ) : (
                <LikertScalePage debate={debate} opinion={opinion} setDebate={setDebate} />
            )}
        </div>
    );
};

export default App;

