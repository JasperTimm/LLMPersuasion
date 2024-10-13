import React, { useEffect, useState } from 'react';
import { axiosInstance } from '../config';
import '../styles/ResultsPage.css';

const ResultsPage = () => {
    const [results, setResults] = useState([]);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState('');
    const [participant, setParticipant] = useState(null);
    const [expandedResultIndex, setExpandedResultIndex] = useState(null);
    const [completionLink, setCompletionLink] = useState('');

    const toggleDebateLogs = (index) => {
        setExpandedResultIndex(expandedResultIndex === index ? null : index);
    };

    useEffect(() => {
        fetchResults();
    }, []);

    const fetchResults = async () => {
        setError('');
        try {
            const response = await axiosInstance.get('/get_results');
            setResults(response.data.results);
            if (response.data.results.length > 0 && response.data.participant) {
                setParticipant(response.data.participant);
                const code = response.data.participant.participantStatus.completion_code;
                setCompletionLink(`https://app.prolific.com/submissions/complete?cc=${code}`);
            }
        } catch (error) {
            console.error("Error fetching results:", error);
            setError('Failed to fetch results. Please try again.');
        }
    };

    const generateResults = async () => {
        setLoading(true);
        setError('');
        try {
            await axiosInstance.post('/generate_results');
            fetchResults();
        } catch (error) {
            console.error("Error generating results:", error);
            setError('Failed to generate results.');
        } finally {
            setLoading(false);
        }
    };

    const getRatingClass = (rating) => {
        switch (rating[0]) {
            case 'A': return 'rating-a';
            case 'B': return 'rating-b';
            case 'C': return 'rating-c';
            case 'D': return 'rating-d';
            case 'E': return 'rating-e';
            case 'F': return 'rating-f';
            default: return '';
        }
    };

    return (
        <div className="results-container">
            <h2 className="results-title">Your Debate Results</h2>
            {participant && (
                <div className={`participant-status`}>
                    <h3>Study completed</h3>
                    <p>Thanks for participating in the study!</p>
                    <p>Please click <a href={completionLink} target="_blank" rel="noreferrer">here</a> to complete the study in {participant.participantService}.</p>
                    <p>If the link does not work, please use the following code: <strong>{participant.participantStatus.completion_code}</strong>.</p>
                </div>
            )}
            {loading ? (
                <p>Generating results... this could take a while.</p>
            ) : results.length === 0 ? (
                <div className="center-button">
                    <button onClick={generateResults}>Get my results!</button>
                    <p><strong>Paid participants: </strong> completion code will appear after results are generated.</p>
                </div>
            ) : (
                results.map((result, index) => (
                    <div key={index} className="result-box">
                        <div className="topic-container">
                            <p className="topic-title"><strong>Topic:</strong> {result.topicDescription}</p>
                        </div>
                        {result.requiresReview ? (
                            <p>This debate requires manual reviewing.</p>
                        ) : result.llmDebateType.startsWith('argument') ? (
                            <p>This topic involved simply reading a passage. There are no results to display.</p>
                        ) : (
                            <>
                                <button onClick={() => toggleDebateLogs(index)}>
                                    {expandedResultIndex === index ? 'Hide Debate Logs' : 'Show Debate Logs'}
                                </button>
                                {expandedResultIndex === index && (
                                    <div className="debate-logs">
                                        {['intro', 'rebuttal', 'conclusion'].map((phase) => (
                                            <div key={phase} className="debate-log-phase">
                                                <h3>{phase.charAt(0).toUpperCase() + phase.slice(1)}</h3>
                                                <div className="responses-container">
                                                    <div className="user-ai-responses">
                                                        <p><strong>User Response:</strong> {result.userResponses[phase]}</p>
                                                        <p><strong>AI Response:</strong> {result.aiResponses[phase]}</p>
                                                    </div>
                                                    {result.chatHistory && result.chatHistory[phase] && (
                                                        <div className="chat-history">
                                                            <h4>AI Agents' Chat</h4>
                                                            {['personalised agent', 'stats agent', 'executive agent'].map((agent, chatIndex) => (
                                                                <p key={chatIndex}><strong>{agent}:</strong> {result.chatHistory[phase][agent]}</p>
                                                            ))}
                                                        </div>
                                                    )}
                                                </div>
                                            </div>
                                        ))}
                                    </div>
                                )}
                                <div className="sides-container">
                                    <div className="side user-side">
                                        <h3>User</h3>
                                        <p>{result.userSide}</p>
                                        <div className="rating-container">
                                            <h4>Results</h4>
                                            <div className={`rating-circle ${getRatingClass(result.userRating)}`}>
                                                {result.userRating}
                                            </div>
                                        </div>
                                    </div>
                                    <div className="side ai-side">
                                        <h3>AI ({result.llmDebateType})</h3>
                                        <p>{result.aiSide}</p>
                                        <div className="rating-container">
                                            <h4>Results</h4>
                                            <div className={`rating-circle ${getRatingClass(result.aiRating)}`}>
                                                {result.aiRating}
                                            </div>
                                        </div>
                                    </div>
                                </div>
                                <div className="feedback-container">
                                    <h3>Feedback</h3>
                                    <p><strong>What went well:</strong> {result.feedback.what_went_well}</p>
                                    <hr />
                                    <p><strong>What to improve:</strong> {result.feedback.what_to_improve}</p>
                                </div>
                            </>
                        )}
                    </div>
                ))
            )}            
            {error && <p className="error-message">{error}</p>}
        </div>
    );
};

export default ResultsPage;