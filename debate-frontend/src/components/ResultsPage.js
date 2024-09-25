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
                        <p><strong>Topic Description:</strong> {result.topicDescription}</p>
                        <p><strong>User Side:</strong> {result.userSide}</p>
                        <p><strong>AI Side:</strong> {result.aiSide}</p>
                        {result.requiresReview ? (
                            <p>This debate requires manual reviewing.</p>
                        ) : (
                            <>
                                <p><strong>Debate ID:</strong> {result.debateId}</p>
                                <p><strong>User Rating:</strong> {result.userRating}</p>
                                <p><strong>AI Rating:</strong> {result.aiRating}</p>
                                <p><strong>Time Spent:</strong> {result.timeSpent} seconds</p>
                                <p><strong>Feedback:</strong> {result.feedback}</p>
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