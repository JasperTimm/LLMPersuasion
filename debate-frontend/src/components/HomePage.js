import React from 'react';
import StartPage from './StartPage';
import OpinionPage from './OpinionPage';
import LikertScalePage from './LikertScalePage';
import DebateFormPage from './DebateFormPage';

const HomePage = ({ debate, setDebate, opinion, setOpinion, history, setHistory, updateDebate, resetDebate }) => {
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

export default HomePage;