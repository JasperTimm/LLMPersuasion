import React, { useState } from 'react';
import DebateForm from './components/DebateForm';
import DebateHistory from './components/DebateHistory';
import DebateInput from './components/DebateInput';

const App = () => {
    const [debate, setDebate] = useState(null);
    const [history, setHistory] = useState([]);

    const updateDebate = (data) => {
        setHistory([...history, { role: 'User', message: data.user_message }, { role: 'AI', message: data.llm_response }]);
        setDebate({ ...debate, state: data.state });
    };

    return (
        <div>
            <h1>Debate Platform</h1>
            {!debate ? (
                <DebateForm setDebate={setDebate} />
            ) : (
                <div>
                    <h2>Topic: {debate.topic}</h2>
                    <DebateHistory history={history} />
                    {debate.state !== 'finished' && <DebateInput debateId={debate.debate_id} updateDebate={updateDebate} />}
                </div>
            )}
        </div>
    );
};

export default App;
