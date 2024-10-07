import React, { useState } from 'react';
import { axiosInstance } from '../config';
import '../styles/QuizPage.css';

const QuizPage = ({ setQuizCompleted, onBackToInstructions }) => {
    const [selectedAnswer1, setSelectedAnswer1] = useState(null);
    const [selectedAnswer2, setSelectedAnswer2] = useState(null);
    const [selectedAnswer3, setSelectedAnswer3] = useState(null);
    const [selectedAnswer4, setSelectedAnswer4] = useState(null);
    const [selectedAnswer5, setSelectedAnswer5] = useState(null);

    const [question1Error, setQuestion1Error] = useState(false);
    const [question2Error, setQuestion2Error] = useState(false);
    const [question3Error, setQuestion3Error] = useState(false);
    const [question4Error, setQuestion4Error] = useState(false);
    const [question5Error, setQuestion5Error] = useState(false);

    const [question1Correct, setQuestion1Correct] = useState(false);
    const [question2Correct, setQuestion2Correct] = useState(false);
    const [question3Correct, setQuestion3Correct] = useState(false);
    const [question4Correct, setQuestion4Correct] = useState(false);
    const [question5Correct, setQuestion5Correct] = useState(false);

    const correctAnswer1 = 'C';
    const correctAnswer2 = 'A';
    const correctAnswer3 = 'B';
    const correctAnswer4 = 'C';
    const correctAnswer5 = 'A';

    const handleSubmit = async (e) => {
        e.preventDefault();
        let allCorrect = true;

        // Check Question 1
        if (selectedAnswer1 !== correctAnswer1) {
            setQuestion1Error(true);
            setQuestion1Correct(false);
            allCorrect = false;
        } else {
            setQuestion1Error(false);
            setQuestion1Correct(true);
        }

        // Check Question 2
        if (selectedAnswer2 !== correctAnswer2) {
            setQuestion2Error(true);
            setQuestion2Correct(false);
            allCorrect = false;
        } else {
            setQuestion2Error(false);
            setQuestion2Correct(true);
        }

        // Check Question 3
        if (selectedAnswer3 !== correctAnswer3) {
            setQuestion3Error(true);
            setQuestion3Correct(false);
            allCorrect = false;
        } else {
            setQuestion3Error(false);
            setQuestion3Correct(true);
        }

        // Check Question 4
        if (selectedAnswer4 !== correctAnswer4) {
            setQuestion4Error(true);
            setQuestion4Correct(false);
            allCorrect = false;
        } else {
            setQuestion4Error(false);
            setQuestion4Correct(true);
        }

        // Check Question 5
        if (selectedAnswer5 !== correctAnswer5) {
            setQuestion5Error(true);
            setQuestion5Correct(false);
            allCorrect = false;
        } else {
            setQuestion5Error(false);
            setQuestion5Correct(true);
        }

        if (allCorrect) {
            setQuizCompleted(true);
            try {
                await axiosInstance.post('/update_quiz_completion', { quiz_completed: true });
            } catch (error) {
                console.error('Failed to update quiz completion status:', error);
            }
        }
    };

    return (
        <div>
            <form onSubmit={handleSubmit}>
                <h1>Quiz</h1>
                {/* Question 1 */}
                <div>
                    <h4 className='question'>Question 1: What is the recommended word count for responses?</h4>
                    <label className='answer-option'>
                        <input 
                            type="radio" 
                            name="question1" 
                            value="A" 
                            checked={selectedAnswer1 === 'A'} 
                            onChange={(e) => setSelectedAnswer1(e.target.value)} 
                        />
                        A) At least 300 words
                    </label>
                    <label className='answer-option'>
                        <input 
                            type="radio" 
                            name="question1" 
                            value="B" 
                            checked={selectedAnswer1 === 'B'} 
                            onChange={(e) => setSelectedAnswer1(e.target.value)} 
                        />
                        B) 50-100 words
                    </label>
                    <label className='answer-option'>
                        <input 
                            type="radio" 
                            name="question1" 
                            value="C" 
                            checked={selectedAnswer1 === 'C'} 
                            onChange={(e) => setSelectedAnswer1(e.target.value)} 
                        />
                        C) 100-200 words
                    </label>
                    <label className='answer-option'>
                        <input 
                            type="radio" 
                            name="question1" 
                            value="D" 
                            checked={selectedAnswer1 === 'D'} 
                            onChange={(e) => setSelectedAnswer1(e.target.value)} 
                        />
                        D) Word count doesn’t matter as long as the response is well-written.
                    </label>
                    {question1Error && <span style={{ color: 'red' }} className="error">Incorrect. Please go back to the instructions page and try again.</span>}
                    {question1Correct && <span style={{ color: 'green' }}>Correct!</span>}
                </div>

                {/* Question 2 */}
                <div>
                    <h4 className='question'>Question 2: Which of the following is the most important guideline when writing your response?</h4>
                    <label className='answer-option'>
                        <input 
                            type="radio" 
                            name="question2" 
                            value="A" 
                            checked={selectedAnswer2 === 'A'} 
                            onChange={(e) => setSelectedAnswer2(e.target.value)} 
                        />
                        A) Stick closely to the debate topic and address it directly.
                    </label>
                    <label className='answer-option'>
                        <input 
                            type="radio" 
                            name="question2" 
                            value="B" 
                            checked={selectedAnswer2 === 'B'} 
                            onChange={(e) => setSelectedAnswer2(e.target.value)} 
                        />
                        B) Use as many complex words as possible to sound knowledgeable.
                    </label>
                    <label className='answer-option'>
                        <input 
                            type="radio" 
                            name="question2" 
                            value="C" 
                            checked={selectedAnswer2 === 'C'} 
                            onChange={(e) => setSelectedAnswer2(e.target.value)} 
                        />
                        C) Try to agree with the LLM’s point of view.
                    </label>
                    <label className='answer-option'>
                        <input 
                            type="radio" 
                            name="question2" 
                            value="D" 
                            checked={selectedAnswer2 === 'D'} 
                            onChange={(e) => setSelectedAnswer2(e.target.value)} 
                        />
                        D) Responses should be longer than your opponent’s to appear more thorough.
                    </label>
                    {question2Error && <span style={{ color: 'red' }} className="error">Incorrect. Please go back to the instructions page and try again.</span>}
                    {question2Correct && <span style={{ color: 'green' }}>Correct!</span>}
                </div>

                {/* Question 3 */}
                <div>
                    <h4 className='question'>Question 3: When giving your opinion in the debate, what should you do?</h4>
                    <label className='answer-option'>
                        <input 
                            type="radio" 
                            name="question3" 
                            value="A" 
                            checked={selectedAnswer3 === 'A'} 
                            onChange={(e) => setSelectedAnswer3(e.target.value)} 
                        />
                        A) State your opinion and move on.
                    </label>
                    <label className='answer-option'>
                        <input 
                            type="radio" 
                            name="question3" 
                            value="B" 
                            checked={selectedAnswer3 === 'B'} 
                            onChange={(e) => setSelectedAnswer3(e.target.value)} 
                        />
                        B) Provide reasons to support your opinion.
                    </label>
                    <label className='answer-option'>
                        <input 
                            type="radio" 
                            name="question3" 
                            value="C" 
                            checked={selectedAnswer3 === 'C'} 
                            onChange={(e) => setSelectedAnswer3(e.target.value)} 
                        />
                        C) Focus on criticizing your opponent’s argument only.
                    </label>
                    <label className='answer-option'>
                        <input 
                            type="radio" 
                            name="question3" 
                            value="D" 
                            checked={selectedAnswer3 === 'D'} 
                            onChange={(e) => setSelectedAnswer3(e.target.value)} 
                        />
                        D) Keep your opinion short and sweet to save time.
                    </label>
                    {question3Error && <span style={{ color: 'red' }} className="error">Incorrect. Please go back to the instructions page and try again.</span>}
                    {question3Correct && <span style={{ color: 'green' }}>Correct!</span>}
                </div>

                {/* Question 4 */}
                <div>
                    <h4 className='question'>Question 4: What is expected regarding the use of AI-generated content in your responses?</h4>
                    <label className='answer-option'>
                        <input
                            type="radio"
                            value="A"
                            checked={selectedAnswer4 === 'A'}
                            onChange={() => setSelectedAnswer4('A')}
                        />
                        A) AI-generated content is allowed as long as you review it.
                    </label>
                    <label className='answer-option'>
                        <input
                            type="radio"
                            value="B"
                            checked={selectedAnswer4 === 'B'}
                            onChange={() => setSelectedAnswer4('B')}
                        />
                        B) AI-generated content is encouraged for creativity.
                    </label>
                    <label className='answer-option'>
                        <input
                            type="radio"
                            value="C"
                            checked={selectedAnswer4 === 'C'}
                            onChange={() => setSelectedAnswer4('C')}
                        />
                        C) AI-generated content is not allowed, and responses must be your own thoughts.
                    </label>
                    <label className='answer-option'>
                        <input
                            type="radio"
                            value="D"
                            checked={selectedAnswer4 === 'D'}
                            onChange={() => setSelectedAnswer4('D')}
                        />
                        D) You can use AI-generated content if you cite the source.
                    </label>
                    {question4Error && <span style={{ color: 'red' }} className="error">Incorrect. Please go back to the instructions page and try again.</span>}
                    {question4Correct && <span style={{ color: 'green' }}>Correct!</span>}
                </div>

                {/* Question 5 */}
                <div>
                    <h4 className='question'>Question 5: What should you do while participating in the debate?</h4>
                    <label className='answer-option'>
                        <input
                            type="radio"
                            value="A"
                            checked={selectedAnswer5 === 'A'}
                            onChange={() => setSelectedAnswer5('A')}
                        />
                        A) Stay on the debate page without navigating away.
                    </label>
                    <label className='answer-option'>
                        <input
                            type="radio"
                            value="B"
                            checked={selectedAnswer5 === 'B'}
                            onChange={() => setSelectedAnswer5('B')}
                        />
                        B) Open another tab to read articles about the topic.
                    </label>
                    <label className='answer-option'>
                        <input
                            type="radio"
                            value="C"
                            checked={selectedAnswer5 === 'C'}
                            onChange={() => setSelectedAnswer5('C')}
                        />
                        C) Leave the page as long as you like.
                    </label>
                    <label className='answer-option'>
                        <input
                            type="radio"
                            value="D"
                            checked={selectedAnswer5 === 'D'}
                            onChange={() => setSelectedAnswer5('D')}
                        />
                        D) Respond after taking a break from the debate.
                    </label>
                    {question5Error && <span style={{ color: 'red' }} className="error">Incorrect. Please go back to the instructions page and try again.</span>}
                    {question5Correct && <span style={{ color: 'green' }}>Correct!</span>}
                </div>

                <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center' }}>
                    <button type="submit">Submit</button>
                    {/* Button to go back to instructions */}
                    <button onClick={onBackToInstructions} style={{ marginTop: '10px' }}>Back to Instructions</button>
                </div>
            </form>
        </div>
    );
};

export default QuizPage;
