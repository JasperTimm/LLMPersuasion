import React, { useState } from 'react';

const QuizPage = ({ setQuizCompleted, onBackToInstructions }) => {
    const [selectedAnswer1, setSelectedAnswer1] = useState(null);
    const [selectedAnswer2, setSelectedAnswer2] = useState(null);
    const [selectedAnswer3, setSelectedAnswer3] = useState(null);

    const [question1Error, setQuestion1Error] = useState(false);
    const [question2Error, setQuestion2Error] = useState(false);
    const [question3Error, setQuestion3Error] = useState(false);

    const [question1Correct, setQuestion1Correct] = useState(false);
    const [question2Correct, setQuestion2Correct] = useState(false);
    const [question3Correct, setQuestion3Correct] = useState(false);

    const correctAnswer1 = 'C';
    const correctAnswer2 = 'A';
    const correctAnswer3 = 'B';

    const handleSubmit = (e) => {
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

        if (allCorrect) {
            setQuizCompleted(true);
        }
    };

    return (
        <div>
            <h2>Quiz Page</h2>

            <form onSubmit={handleSubmit}>
                {/* Question 1 */}
                <div>
                    <h4>Question 1: What is the recommended word count for responses?</h4>
                    <label>
                        <input 
                            type="radio" 
                            name="question1" 
                            value="A" 
                            checked={selectedAnswer1 === 'A'} 
                            onChange={(e) => setSelectedAnswer1(e.target.value)} 
                        />
                        A) At least 300 words
                    </label><br />
                    <label>
                        <input 
                            type="radio" 
                            name="question1" 
                            value="B" 
                            checked={selectedAnswer1 === 'B'} 
                            onChange={(e) => setSelectedAnswer1(e.target.value)} 
                        />
                        B) 50-100 words
                    </label><br />
                    <label>
                        <input 
                            type="radio" 
                            name="question1" 
                            value="C" 
                            checked={selectedAnswer1 === 'C'} 
                            onChange={(e) => setSelectedAnswer1(e.target.value)} 
                        />
                        C) 100-200 words
                    </label><br />
                    <label>
                        <input 
                            type="radio" 
                            name="question1" 
                            value="D" 
                            checked={selectedAnswer1 === 'D'} 
                            onChange={(e) => setSelectedAnswer1(e.target.value)} 
                        />
                        D) Word count doesn’t matter as long as the response is well-written.
                    </label><br />
                    {question1Error && <span style={{ color: 'red' }} className="error">Incorrect. Please go back to the instructions page and try again.</span>}
                    {question1Correct && <span style={{ color: 'green' }}>Correct!</span>}
                </div>

                {/* Question 2 */}
                <div>
                    <h4>Question 2: Which of the following is the most important guideline when writing your response?</h4>
                    <label>
                        <input 
                            type="radio" 
                            name="question2" 
                            value="A" 
                            checked={selectedAnswer2 === 'A'} 
                            onChange={(e) => setSelectedAnswer2(e.target.value)} 
                        />
                        A) Stick closely to the debate topic and address it directly.
                    </label><br />
                    <label>
                        <input 
                            type="radio" 
                            name="question2" 
                            value="B" 
                            checked={selectedAnswer2 === 'B'} 
                            onChange={(e) => setSelectedAnswer2(e.target.value)} 
                        />
                        B) Use as many complex words as possible to sound knowledgeable.
                    </label><br />
                    <label>
                        <input 
                            type="radio" 
                            name="question2" 
                            value="C" 
                            checked={selectedAnswer2 === 'C'} 
                            onChange={(e) => setSelectedAnswer2(e.target.value)} 
                        />
                        C) Try to agree with the LLM’s point of view.
                    </label><br />
                    <label>
                        <input 
                            type="radio" 
                            name="question2" 
                            value="D" 
                            checked={selectedAnswer2 === 'D'} 
                            onChange={(e) => setSelectedAnswer2(e.target.value)} 
                        />
                        D) Responses should be longer than your opponent’s to appear more thorough.
                    </label><br />
                    {question2Error && <span style={{ color: 'red' }} className="error">Incorrect. Please go back to the instructions page and try again.</span>}
                    {question2Correct && <span style={{ color: 'green' }}>Correct!</span>}
                </div>

                {/* Question 3 */}
                <div>
                    <h4>Question 3: When giving your opinion in the debate, what should you do?</h4>
                    <label>
                        <input 
                            type="radio" 
                            name="question3" 
                            value="A" 
                            checked={selectedAnswer3 === 'A'} 
                            onChange={(e) => setSelectedAnswer3(e.target.value)} 
                        />
                        A) State your opinion and move on.
                    </label><br />
                    <label>
                        <input 
                            type="radio" 
                            name="question3" 
                            value="B" 
                            checked={selectedAnswer3 === 'B'} 
                            onChange={(e) => setSelectedAnswer3(e.target.value)} 
                        />
                        B) Provide reasons and examples to support your opinion.
                    </label><br />
                    <label>
                        <input 
                            type="radio" 
                            name="question3" 
                            value="C" 
                            checked={selectedAnswer3 === 'C'} 
                            onChange={(e) => setSelectedAnswer3(e.target.value)} 
                        />
                        C) Focus on criticizing your opponent’s argument only.
                    </label><br />
                    <label>
                        <input 
                            type="radio" 
                            name="question3" 
                            value="D" 
                            checked={selectedAnswer3 === 'D'} 
                            onChange={(e) => setSelectedAnswer3(e.target.value)} 
                        />
                        D) Keep your opinion short and sweet to save time.
                    </label><br />
                    {question3Error && <span style={{ color: 'red' }} className="error">Incorrect. Please go back to the instructions page and try again.</span>}
                    {question3Correct && <span style={{ color: 'green' }}>Correct!</span>}
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
