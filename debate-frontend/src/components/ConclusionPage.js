import React, { useState } from 'react';
import { axiosInstance } from '../config';
import '../styles/NewUserPage.css';

function ConclusionPage({ user, setUser }) {
    const [isScrolledToBottom, setIsScrolledToBottom] = useState(false);
    const [isChecked, setIsChecked] = useState(false);

    const handleScroll = (e) => {
        const { scrollTop, scrollHeight, clientHeight } = e.target;
        if (scrollTop + clientHeight >= scrollHeight - 1) {
            setIsScrolledToBottom(true);
        }
    };

    const concludeStudy = async () => {
        try {
            await axiosInstance.post(`/conclude`);
            setUser({ ...user, concluded: true });
        } catch (error) {
            console.error("Error concluding study:", error);
        }
    };

    return (
        <div className="container">
            <h1>Thank You for Your Participation!</h1>
            <div className="consent-container" onScroll={handleScroll}>
                <p>We deeply appreciate your time and effort in participating in our study. Your contribution is invaluable to advancing our understanding of how Large Language Models (LLMs) can influence opinions. Below, we’ve outlined important information that you should consider before you leave.</p>

                <h2>Talking with Others</h2>
                <p><strong>Most important:</strong> Please do not discuss the details of this study with other participants who have not yet completed it. If you know someone who is in the middle of their participation or is likely to join the study, it’s crucial that you avoid sharing any information with them. This is essential to maintain the integrity of the study. However, if you encounter others who have finished, feel free to discuss your experiences.</p>

                <h2>Misleading Statistics</h2>
                <p>It’s important to understand that some of the statistics and sources you encountered during your debates were intentionally fabricated. Beyond the usual AI “hallucinations” (when the AI generates non-existent information), we specifically instructed the AI to invent statistics if real ones were not available, and to cite sources that may not exist. If you found certain statistics compelling, we encourage you to revisit your opinions on those topics. This aspect of the study was designed to highlight how easily misinformation can spread, especially online. Always be cautious when someone quotes statistics on the internet without credible sources.</p>

                <h2>The Study’s Purpose</h2>
                <p>Our goal was to explore how effectively we can change people's opinions on various topics through debates with different types of LLMs. We’ve based our methodology on previous research and designed several debate types to assess which methods are most persuasive:</p>
                <ul>
                    <li><strong>Argument:</strong> In some instances, you were presented with a pre-constructed argument rather than engaging in a debate. This served as a control to measure the impact of active versus passive persuasion.</li>
                    <li><strong>Simple:</strong> This type of LLM was given a basic prompt to debate with you, without any special instructions or data. Its sole task was to convince you to change your mind.</li>
                    <li><strong>Stats:</strong> This LLM was directed to use data and statistics in its arguments, making the stats appear realistic and citing sources that seemed credible. If relevant statistics were not available, the AI was allowed to create them.</li>
                    <li><strong>Personalised:</strong> This LLM tailored its arguments based on your demographics and personality traits, aiming to persuade you with content specifically designed for you.</li>
                    <li><strong>Mixed:</strong> This approach combined the strategies of the Stats and Personalised LLMs. These AIs discussed the response in a private chat, and an executive agent then summarised the discussion to generate the debate response.</li>
                </ul>
                <p>If you completed all five debates, you encountered each of these types. If you didn’t finish all the debates, you may have only interacted with a few.</p>

                <h2>Debriefing and Reflection</h2>
                <p>We encourage you to take some time to reflect on your experience in this study. Consider how your opinions may have changed and whether the arguments or statistics you encountered genuinely altered your views or merely seemed persuasive at the moment. This study aimed to demonstrate how easily opinions can be influenced, often with misleading or fabricated information. Revisiting your stance on the debated topics after some time might help solidify your true beliefs.</p>

                <h2>Questions, Concerns, and Consent Withdrawal</h2>
                <p>If you have any questions or concerns about your participation in this study, or if you wish to discuss any aspect of the study further, please don’t hesitate to reach out to us. Additionally, if you’d like to withdraw consent for your participation you can contact us regarding this too - <strong>you’ll need to give us the userid you were given as we have no way of looking you up otherwise.</strong> You can contact us at: <a href="mailto:jasper.timm@gmail.com">jasper.timm@gmail.com</a></p>

                <h2>Further Reading and Resources</h2>
                <p>To better understand the topics covered in this study and to protect yourself from misinformation, we recommend the following resources:</p>
                <ul>
                    <li><a href="https://foundation.mozilla.org/en/internet-health-report/2022/">The Mozilla Foundation’s Internet Health Report 2022 (AI)</a>: An annual report that explores issues like misinformation, data privacy, and the impact of AI on society.</li>
                    <li>“Critical Thinking: Tools for Taking Charge of Your Learning and Your Life” by Richard Paul and Linda Elder: A book that explores the foundations of critical thinking and its application in daily life.</li>
                </ul>

                <h2>Results</h2>
                <p>On the following page, you’ll be able to view the results of your debates. <em>(This page is still a work in progress)</em></p>

                <h2>Thank You Once Again</h2>
                <p>Thank you once again for participating in our study. Your involvement is helping us better understand the effects of LLMs on public opinion and contributes to the ongoing research in AI and its influence on society.</p>
                                
            </div>
            <div className="consent-actions">
                <label className={isScrolledToBottom ? 'label-bold' : 'label-unbold'}>
                    <input
                        type="checkbox"
                        disabled={!isScrolledToBottom}
                        className={!isScrolledToBottom ? 'checkbox-disabled' : ''}
                        checked={isChecked}
                        onChange={(e) => setIsChecked(e.target.checked)}
                    />
                    I have read and understood the above
                </label>
                <button
                    type="button"
                    disabled={!isChecked}
                    onClick={concludeStudy}
                >
                    Submit
                </button>
            </div>
        </div>
    );
}

export default ConclusionPage;