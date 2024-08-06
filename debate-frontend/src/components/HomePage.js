import React from 'react';
import StartPage from './StartPage';
import OpinionPage from './OpinionPage';
import LikertScalePage from './LikertScalePage';
import DebateFormPage from './DebateFormPage';
import FinalOpinionPage from './FinalOpinionPage';
import FinalLikertScalePage from './FinalLikertScalePage';

const HomePage = ({ debate, setDebate, debateHistory, chatHistory, updateDebate, resetDebate }) => {
    return (
        <div>
            <h1>Debate Platform</h1>
            {!debate ? (
                <StartPage setDebate={setDebate} />
            ) : !debate.initial_opinion ? (
                <OpinionPage debate={debate} setDebate={setDebate} />
            ) : !debate.initial_likert_score ? (
                <LikertScalePage debate={debate} setDebate={setDebate} />
            ) : debate.state !== 'final_opinion' ? (
                <DebateFormPage debate={debate} debateHistory={debateHistory} chatHistory={chatHistory} updateDebate={updateDebate} />
            ) : !debate.final_opinion ? (
                <FinalOpinionPage debate={debate} setDebate={setDebate} />
            ) : (
                <FinalLikertScalePage debate={debate} resetDebate={resetDebate} />
            )}
        </div>
    );
};

export default HomePage;