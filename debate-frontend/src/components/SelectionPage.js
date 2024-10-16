import React, { useState } from 'react';
import { axiosInstance } from '../config';

const SelectionPage = ({ setDebate }) => {
    const [llmModelType, setLlmModelType] = useState('openai_gpt-4o-mini');
    const [llmDebateType, setLlmDebateType] = useState('simple');

    const startDebateAdmin = async () => {
        try {
            const response = await axiosInstance.post(`/start_debate_admin`, { 
                llm_model_type: llmModelType,
                llm_debate_type: llmDebateType
            });
            setDebate(response.data);
        } catch (error) {
            console.error("Error starting debate:", error);
        }
    };

    return (
        <div className="container">
            <label>
                Select LLM Model:
                <select value={llmModelType} onChange={(e) => setLlmModelType(e.target.value)}>
                    <option value="openai_gpt-4o-mini">OpenAI GPT-4o-mini</option>
                    <option value="local_llama3">Local LLaMA3</option>
                </select>
            </label>
            <label>
                Select LLM Debate Type:
                <select value={llmDebateType} onChange={(e) => setLlmDebateType(e.target.value)}>
                    <option value="argument">Argument</option>
                    <option value="argumentllm">Argument LLM</option>
                    <option value="simple">Simple</option>
                    <option value="stats">Statistics</option>
                    <option value="personalized">Personalized</option>
                    <option value="mixed">Mixed</option>
                </select>
            </label>
            <button onClick={startDebateAdmin}>Start Debate</button>
        </div>
    );
};

export default SelectionPage;