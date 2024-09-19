import React, { useEffect, useState } from 'react';
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
import { axiosInstance } from '../config';

const MainPage = ({ debate, startDebate, setDebate, debateHistory, chatHistory, updateDebate, user, setUser, resetDebate, errorStartDebate }) => {
    const [currentPage, setCurrentPage] = useState('');

    useEffect(() => {
        const handlePaste = (event) => {
            const data = event.clipboardData.getData('Text');
            const type = 'paste'

            axiosInstance.post('/log_event', {
                data,
                'currentPage': currentPage === 'DebateFormPage' ? currentPage + ':' + debate.state : currentPage,
                type,
            }).catch(error => {
                // Fail silently
            });
        };
        const handleCopy = (event) => {
            const data = window.getSelection().toString();
            const type = 'copy'

            axiosInstance.post('/log_event', {
                data,
                'currentPage': currentPage === 'DebateFormPage' ? currentPage + ':' + debate.state : currentPage,
                type,
            }).catch(error => {
                // Fail silently
            });
        };

        document.addEventListener('paste', handlePaste);
        document.addEventListener('copy', handleCopy);

        return () => {
            document.removeEventListener('paste', handlePaste);
            document.removeEventListener('copy', handleCopy);
        };
    }, [currentPage, debate]);

    useEffect(() => {
        if (!debate && user.admin) {
            setCurrentPage('SelectionPage');
        } else if (!debate) {
            setCurrentPage('StartDebatePage');
        } else if (!debate.initial_opinion) {
            setCurrentPage('OpinionPage');
        } else if (!debate.initial_likert_score) {
            setCurrentPage('LikertScalePage');
        } else if (debate.argument && debate.state !== 'final_opinion') {
            setCurrentPage('ArgumentPage');
        } else if (debate.state !== 'final_opinion') {
            setCurrentPage('DebateFormPage');
        } else if (!debate.final_opinion) {
            setCurrentPage('FinalOpinionPage');
        } else if (!debate.final_likert_score) {
            setCurrentPage('FinalLikertScalePage');
        } else {
            setCurrentPage('ContinuePage');
        }
        
    }, [debate, user]);

    return (
        <div className='main-page-container'>
            <h1>Debate Platform</h1>
            {   debate && debate.topic ? (
                <div className="debate-topic">
                    <span className="debate-topic-label">Debate Topic:</span>
                    <span>{debate.topic}</span>
                </div>
            ) : null}
            {   currentPage === 'SelectionPage' ? (
                <SelectionPage setDebate={setDebate} />
            ) : currentPage === 'StartDebatePage' ? (
                <StartDebatePage startDebate={startDebate} errorStartDebate={errorStartDebate} />
            ) : currentPage === 'OpinionPage' ? (
                <OpinionPage debate={debate} setDebate={setDebate} />
            ) : currentPage === 'LikertScalePage' ? (
                <LikertScalePage debate={debate} setDebate={setDebate} />
            ) : currentPage === 'ArgumentPage' ? (
                <ArgumentPage debate={debate} setDebate={setDebate} />
            ) : currentPage === 'DebateFormPage' ? (
                <DebateFormPage debate={debate} debateHistory={debateHistory} chatHistory={chatHistory} updateDebate={updateDebate} />
            ) : currentPage === 'FinalOpinionPage' ? (
                <FinalOpinionPage debate={debate} setDebate={setDebate} />
            ) : currentPage === 'FinalLikertScalePage' ? (
                <FinalLikertScalePage debate={debate} setDebate={setDebate} user={user} setUser={setUser} />
            ) : (
                <ContinuePage startDebate={startDebate} user={user} setUser={setUser} resetDebate={resetDebate} />
            )} 
        </div>
    );
};

export default MainPage;