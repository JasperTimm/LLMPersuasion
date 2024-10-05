import React from 'react';
import '../styles/InstructionPage.css';

const InstructionPage = ({ onContinue }) => {
  return (
    <div className="instruction-page">
      <h1>Instructions for Responding</h1>
      <p>Before you begin, please read the following guidelines for participating in the debate:</p>
      <ol>
        <li>
          <strong>Response Length:</strong> Responses should be <strong>around 100-200 words</strong> in length.
        </li>
        <li>
          <strong>Stay on Topic:</strong> Your response must <strong>address the debate question directly</strong> and remain focused on the topic.
        </li>
        <li>
          <strong>Give Reasons:</strong> Please provide <strong>reasons for your opinions</strong>, not just a simple answer. Support your viewpoint with logic or examples.
        </li>
      </ol>
      <button onClick={onContinue}>Continue to Debate</button>
    </div>
  );
};

export default InstructionPage;
