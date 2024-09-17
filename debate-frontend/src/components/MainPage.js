import React from 'react';
import SelectionPage from './SelectionPage';
import StartDebatePage from './StartDebatePage';
import OpinionPage from './OpinionPage';
import LikertScalePage from './LikertScalePage';
import DebateFormPage from './DebateFormPage';
import FinalOpinionPage from './FinalOpinionPage';
import FinalLikertScalePage from './FinalLikertScalePage';
import ContinuePage from './ContinuePage';
import ArgumentPage from './ArgumentPage';
import '../styles/MainPage.css';

const MainPage = ({ debate, startDebate, setDebate, debateHistory, chatHistory, updateDebate, user, setUser, resetDebate, errorStartDebate }) => {
    return (
        <div className='main-page-container'>
            <h1>Debate Platform</h1>
            {   debate && debate.topic ? (
                <div className="debate-topic">
                    <span className="debate-topic-label">Debate Topic:</span>
                    <span>{debate.topic}</span>
                </div>
            ) : null}
            {   !debate && user.admin ? (
                <SelectionPage setDebate={setDebate} />
            ) : !debate ? (
                <StartDebatePage startDebate={startDebate} errorStartDebate={errorStartDebate} />
            ) : !debate.initial_opinion ? (
                <OpinionPage debate={debate} setDebate={setDebate} />
            ) : !debate.initial_likert_score ? (
                <LikertScalePage debate={debate} setDebate={setDebate} />
            ) : debate.argument && debate.state !== 'final_opinion' ? (
                <ArgumentPage debate={debate} setDebate={setDebate} />
            ) : debate.state !== 'final_opinion' ? (
                <DebateFormPage debate={debate} debateHistory={debateHistory} chatHistory={chatHistory} updateDebate={updateDebate} />
            ) : !debate.final_opinion ? (
                <FinalOpinionPage debate={debate} setDebate={setDebate} />
            ) : !debate.final_likert_score ? (
                <FinalLikertScalePage debate={debate} setDebate={setDebate} user={user} setUser={setUser} />
            ) : (
                <ContinuePage startDebate={startDebate} user={user} setUser={setUser} resetDebate={resetDebate} />
            )} 
        </div>
    );
};

export default MainPage;