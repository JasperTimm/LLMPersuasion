import React, { useState } from 'react';
import { axiosInstance } from '../config';
import '../styles/UserInfoPage.css';

function PersonalityTraitsPage({ demographics, setUserInfoCompleted }) {
    const [personalityTraits, setPersonalityTraits] = useState({
        extravertedEnthusiastic: '',
        criticalQuarrelsome: '',
        dependableSelfDisciplined: '',
        anxiousEasilyUpset: '',
        openToExperiencesComplex: '',
        reservedQuiet: '',
        sympatheticWarm: '',
        disorganizedCareless: '',
        calmEmotionallyStable: '',
        conventionalUncreative: ''
    });
    const [error, setError] = useState('');

    const handlePersonalityTraitChange = (key, value) => {
        setPersonalityTraits({
            ...personalityTraits,
            [key]: value
        });
    };

    const handleSubmit = async () => {
        try {
            await axiosInstance.post('/user_info', {
                ...demographics,
                ...personalityTraits
            });
            setUserInfoCompleted(true);
        } catch (error) {
            setError('Error submitting user information');
        }
    };

    return (
        <div className="container">
            <h2>Personality Traits</h2>
            <div class="instructions">
                <p>
                    Here are a number of personality traits that may or may not apply to you. 
                    Please write a number next to each statement to indicate the extent to which 
                    you agree or disagree with that statement. You should rate the extent to which 
                    the pair of traits applies to you, even if one characteristic applies more 
                    strongly than the other.
                </p>
                <p>
                    <strong>Rating Scale:</strong>
                    <ul>
                        <li>1 = Disagree strongly</li>
                        <li>2 = Disagree moderately</li>
                        <li>3 = Disagree a little</li>
                        <li>4 = Neither agree nor disagree</li>
                        <li>5 = Agree a little</li>
                        <li>6 = Agree moderately</li>
                        <li>7 = Agree strongly</li>
                    </ul>
                </p>
                <p><strong>I see myself as:</strong></p>
            </div>
            <input
                type="number"
                value={personalityTraits.extravertedEnthusiastic}
                onChange={(e) => handlePersonalityTraitChange('extravertedEnthusiastic', e.target.value)}
                placeholder="Extraverted, enthusiastic"
            />
            <input
                type="number"
                value={personalityTraits.criticalQuarrelsome}
                onChange={(e) => handlePersonalityTraitChange('criticalQuarrelsome', e.target.value)}
                placeholder="Critical, quarrelsome"
            />
            <input
                type="number"
                value={personalityTraits.dependableSelfDisciplined}
                onChange={(e) => handlePersonalityTraitChange('dependableSelfDisciplined', e.target.value)}
                placeholder="Dependable, self-disciplined"
            />
            <input
                type="number"
                value={personalityTraits.anxiousEasilyUpset}
                onChange={(e) => handlePersonalityTraitChange('anxiousEasilyUpset', e.target.value)}
                placeholder="Anxious, easily upset"
            />
            <input
                type="number"
                value={personalityTraits.openToExperiencesComplex}
                onChange={(e) => handlePersonalityTraitChange('openToExperiencesComplex', e.target.value)}
                placeholder="Open to experiences, complex"
            />
            <input
                type="number"
                value={personalityTraits.reservedQuiet}
                onChange={(e) => handlePersonalityTraitChange('reservedQuiet', e.target.value)}
                placeholder="Reserved, quiet"
            />
            <input
                type="number"
                value={personalityTraits.sympatheticWarm}
                onChange={(e) => handlePersonalityTraitChange('sympatheticWarm', e.target.value)}
                placeholder="Sympathetic, warm"
            />
            <input
                type="number"
                value={personalityTraits.disorganizedCareless}
                onChange={(e) => handlePersonalityTraitChange('disorganizedCareless', e.target.value)}
                placeholder="Disorganized, careless"
            />
            <input
                type="number"
                value={personalityTraits.calmEmotionallyStable}
                onChange={(e) => handlePersonalityTraitChange('calmEmotionallyStable', e.target.value)}
                placeholder="Calm, emotionally stable"
            />
            <input
                type="number"
                value={personalityTraits.conventionalUncreative}
                onChange={(e) => handlePersonalityTraitChange('conventionalUncreative', e.target.value)}
                placeholder="Conventional, uncreative"
            />
            <button onClick={handleSubmit}>Submit</button>
            {error && <p className="error">{error}</p>}
        </div>
    );
}

export default PersonalityTraitsPage;