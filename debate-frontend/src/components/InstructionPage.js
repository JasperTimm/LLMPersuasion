import React from 'react';
import '../styles/InstructionPage.css';

const InstructionPage = ({ onContinue }) => {
  return (
    <div className="instruction-page">
      <h1>Instructions for Responding</h1>
      <p>Before you begin, please read the following guidelines for participating in the debate:</p>
      <ol>
        <li>
          <strong>Response Length:</strong> Responses <strong>in the debate</strong> should be <strong>around 100-200 words</strong> in length. Responses for opinions need only be one or two sentences.
        </li>
        <li>
          <strong>Stay on Topic:</strong> Your response must <strong>address the debate question directly</strong> and remain focused on the topic.
        </li>
        <li>
          <strong>Give Reasons:</strong> Please provide <strong>reasons for your opinions</strong>, not just a simple answer. Support your viewpoint with examples if possible.
        </li>
        <li>
          <strong>No AI content:</strong> Please <strong>DO NOT use AI generated content</strong>. Your responses should be your own thoughts and opinions. We detect AI content and it may affect your submission.
        </li>
        <li>
          <strong>Remain on the page:</strong> Please <strong>do not navigate away from the page</strong> while participating in the debate. We track your inactive time and it may affect your submission.
        </li>       
      </ol>
      <button onClick={onContinue}>Continue to Quiz</button>
    </div>
  );
};

export default InstructionPage;
