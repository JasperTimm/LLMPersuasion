import React, { useEffect, useState } from 'react';
import { axiosInstance } from '../config';
import '../styles/ResultsPage.css';

const ResultsPage = () => {
    const [results, setResults] = useState([]);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState('');

    useEffect(() => {
        fetchResults();
    }, []);

    const fetchResults = async () => {
        try {
            const response = await axiosInstance.get('/get_results');
            setResults(response.data);
        } catch (error) {
            console.error("Error fetching results:", error);
            setError('Failed to fetch results.');
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
            {loading ? (
                <p>Generating results... this could take a while.</p>
            ) : results.length === 0 ? (
                <div className="center-button">
                    <button onClick={generateResults}>Get my results!</button>
                </div>
            ) : (
                results.map((result, index) => (
                    <div key={index} className="result-box">
                        <div className="topic-container">
                            <p className="topic-title"><strong>Topic:</strong> {result.topicDescription}</p>
                        </div>
                        {result.requiresReview ? (
                            <p>This debate requires manual reviewing.</p>
                        ) : (
                            <>
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
                                        <h3>AI</h3>
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